from tkinter import *
import sqlite3
import re
#create the root
root = Tk()
root.configure(bg="grey")
#creating title and specifiying window size
root.title("Speed Tracker")
root.geometry("400x300")
top = Toplevel()
top.geometry("1000x300")


conn = sqlite3.connect("speeding_cars.db")
c = conn.cursor()
#create table
c.execute("""CREATE TABLE IF NOT EXISTS cars (
            license_plate text,
            speed integer
            )""")
conn.commit()

class SpeedTracker():
    def __init__(self,master,second):
        self.master = master
        master.title("Speed Tracker")

        #creating label widget
        self.label_open = Label(master, text="Welcome to the Speed Tracker!",bg="grey",fg="blue")
        self.label_open.grid(row=0,column=1)

        self.label_result = Label(second, text ="Speed Tracker with existing data",fg="black")
        self.label_result.pack()

        self.time1 = Entry(master,width=5)
        self.time1.grid(row=1,column=1)
        
        self.time2 = Entry(master,width=5)
        self.time2.grid(row=2,column=1)
        
        self.plate = Entry(master,width=15)
        self.plate.grid(row=3,column=1)

        self.time1_label = Label(master, text="First Time",bg="grey",fg="white")
        self.time1_label.grid(row=1,column=0)
        self.time2_label = Label(master, text="Second Time",bg="grey",fg="white")
        self.time2_label.grid(row=2,column=0)
        self.plate_label = Label(master, text="License Plate",bg="grey",fg="white")
        self.plate_label.grid(row=3,column=0)
        

        self.btn_check_speed_master = Button(master,text="Check Speed",fg="blue",command=self.check_speed_master)
        self.btn_check_speed = Button(second,text="Check Speed",fg="red",command=self.check_speed)
        self.btn_check_plate = Button(second,text="Check Plate",fg="red",command=self.check_plate)
        self.btn_check_plate_master = Button(master,text="Check Plate",fg="blue",command=self.check_plate_master)
        self.btn_check_speed.pack()
        self.btn_check_plate.pack()
        self.btn_check_speed_master.grid(row=4,column=1)
        self.btn_check_plate_master.grid(row=5,column=1)

    def check_speed_master(self):
        x = self.time1.get()
        y = self.time2.get()
        int_x = float(x)
        int_y = float(y)
        time_taken = int_y - int_x
        speed = time_taken / 1
        self.msg = "Speed =", speed
        self.label_open["text"] = self.msg

    def check_plate_master(self):
        numberplate = self.plate.get()
        r = re.compile('[A-Z]{2}[0-9]{2}[A-Z]{3}')
        if r.match(numberplate):
            self.msg = "Valid Numberplate"
        else:
            self.msg = 'Invalid Numberplate'
        self.label_open["text"] = self.msg

    def check_speed(self):
        c.execute("SELECT license_plate FROM cars WHERE speed>=?",(70,))
        conn.commit()
        pre_speed = c.fetchall()
        self.msg = "Vehicles over speed limit:",pre_speed
        self.label_result["text"] = self.msg


    def check_plate(self):
        all_n = []
        c.execute("SELECT license_plate FROM cars WHERE speed>=?",(0,))
        conn.commit()
        all_cars = c.fetchall()
        for i in range(len(all_cars)):
            numberplate = all_cars[i][0]
            r = re.compile('[A-Z]{2}[0-9]{2}[A-Z]{3}')
            if r.match(numberplate):
                 all_n.append((numberplate,"valid number plate"))
            else:
                 all_n.append((numberplate,"invalid number plate"))

            self.msg = all_n

        self.label_result["text"] = self.msg

gui = SpeedTracker(root,top)

root.mainloop()
root.destroy()
