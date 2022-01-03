import sqlite3
from datetime import datetime
from datetime import date, timedelta
from os import system

import tkinter as tk
from tkinter import*
from tkinter import ttk
import tkinter.messagebox
from tkinter import simpledialog

def clear():
    system("cls")
# variable names in english
# no upper case or camel case for variable names
# use underscores
conn = sqlite3.connect('birthdays.sqlite')
cur = conn.cursor()


class Library:

    def __init__(self,root):
        self.root = root
        self.root.title("Geburtstagskalender")
        self.root.geometry("500x400")          #1350x750+0+0
        self.root.configure(background = "#fff2cc")


#===================================Frames=====================================


        MainFrame = Frame(self.root,bg='#fff2cc')
        MainFrame.grid()

        geburtstagskind = StringVar()
        days_till_bd = StringVar()
        new_name = StringVar()
        new_date = StringVar()

        def iExit():
            iExit = tkinter.messagebox.askyesno ("Geburtstagskalender","Programm verlassen?")
            if iExit>0:
                root.destroy()
                return

        def days_between(d1, d2):
            d1 = datetime.strptime(d1, "%Y-%m-%d")
            d2 = datetime.strptime(d2, "%Y-%m-%d")
            return abs((d2 - d1).days)

        def getbdlist():

            # fetch a list of all entries in the database

            cur.execute("""

            SELECT * FROM birthdays""")
            newlist=list()
            bds_list = cur.fetchall()
            for index in bds_list:
                for i in index:
                    newlist.append(i)
            print("\nInfo: there are " + str(int((len(newlist)/3))) + " entries in the database\n")


            # loop through the dates

            index = 2

            lowest_days = None
            while index <(len(newlist)):
                #d1 = str('1970-01-01')
                d_beginning_y = date(date.today().year, 1, 1)
                d_beginning_y = str(d_beginning_y)

                # get current year
                d_splitted  = d_beginning_y.split("-")
                current_year = int(d_splitted[0])

                # get date 2 which is the birthday

                d_bd = newlist[index]

                splitted = d_bd.split("-")
                intlist = list()
                for i in splitted:
                    if i == splitted[0]:
                        intlist.append(current_year)
                    else:
                        intlist.append(int(i))
                d_bd_new = str(intlist[0])+ "-" +str(intlist[1])+ "-" + str(intlist[2])


                # get todays date

                d_today = str(date.today())

                difference = days_between(d_today, d_bd_new)
                #print(difference)

                index += 3
                if lowest_days is None or difference < lowest_days:
                    lowest_days = difference
                    get_bd = d_bd

                else:
                    pass

            # Select the closest birthday from the database

            cur.execute(" SELECT * FROM birthdays WHERE birthday = ?", (get_bd,))

            closest_bd = cur.fetchall()

            #print(closest_bd)

            # Print out all names

            lst = list()

            for index in closest_bd:
                for i in index:
                    lst.append(i)
            #print(lst)
            name_bd = lst[1:]
            name = name_bd[0]
            bd = name_bd[1]


            geburtstagskind.set(str(name) + " " + str(bd))
            days_till_bd.set(str(lowest_days))
        getbdlist()


        class input_bd():
            def put(self,secondo):
                cur.execute("""

                INSERT OR IGNORE INTO birthdays (name,birthday) VALUES (?,?)""", (self,secondo))

                conn.commit()

        def put_into_db():

            name_db = new_name.get()
            date_db = new_date.get()
            date_db = str(date_db)

            # check if format is correct

            try:
                format = "%Y-%m-%d"


                datetime.strptime(date_db, format)


            except:
                tkinter.messagebox.showerror("Fehler","Bitte folgendes Format eingeben: YYYY-MM-DD")
                return

            input_bd.put(name_db,date_db)
            tkinter.messagebox.showinfo("Info!","Daten sind in die Datenbank geladen!")

#================= GUI functions ===============================================


        label_1 = Label(MainFrame,font=("Rockwell Extra Bold",20,"normal"),bg='#fff2cc',fg="#000000",text="Geburtstage")
        label_1.grid(row=0,column=0)

        label_space = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000")
        label_space.grid(row=1,column=1)

        label_2 = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000",text="Als nächstes hat Geburtstag: ")
        label_2.grid(row=2,column=0)

        label_3 = Label(MainFrame,font=("Rockwell",12),bg='#fff2cc',fg="#000000",textvariable=geburtstagskind)
        label_3.grid(row=2,column=1)

        label_4 = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000",text="Tag(e) bis dahin: ")
        label_4.grid(row=3,column=0)

        label_5 = Label(MainFrame,font=("Rockwell",12),bg='#fff2cc',fg="#000000",textvariable=days_till_bd)
        label_5.grid(row=3,column=1)


        label_6 = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000", text ="Neuen Namen eingeben: ")
        label_6.grid(row=5,column=0)

        enter_1 = Entry(MainFrame,font=("Rockwell",12),bg='#ffffff',fg="#000000", textvariable=new_name)
        enter_1.grid(row=5,column=1)


        label_7 = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000", text ="Geburtsdatum eingeben: ")
        label_7.grid(row=6,column=0)

        enter_2 = Entry(MainFrame,font=("Rockwell",12),bg='#ffffff',fg="#000000", textvariable=new_date)
        enter_2.grid(row=6,column=1)


        label_space_2 = Label(MainFrame,font=("Rockwell Extra Bold",12),bg='#fff2cc',fg="#000000")
        label_space_2.grid(row=7,column=1)


        button1 = Button(MainFrame,bg='#fff2cc', text ="exit", command = iExit)
        button1.grid(row=8,column=0)

        button2 = Button(MainFrame,bg='#fff2cc', text ="Daten in Datenbank laden", command = put_into_db)
        button2.grid(row=8,column=1)




if __name__=="__main__":
    root = Tk()
    application = Library(root)
    root.mainloop()
