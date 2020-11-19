from datetime import date
import sqlite3
from tkinter import *
import hashlib

def appSetUp():
    global name
    global password
    global setup
    name = nameEntry.get()
    date1 = date.today().strftime("%B %d, %Y")
    password = passwordEntry.get()
    password = hashlib.md5(password.encode())
    print(name," joined Account Tracker on ",date1)

    conn = sqlite3.connect('accountDatabase.db')
    print("DATABASE successfully created ")

    cursor = conn.cursor()

    #SQL OPERATION
    sql ='''CREATE TABLE "USER_LOGIN" (
	"NAME"	TEXT,
	"PASSWORD"	TEXT
    )'''
    cursor.execute(sql)
    print(" User Database created successfully........")
    conn.commit()


    sql = '''CREATE TABLE "ACCOUNT_DATA" (
	"ID"	INTEGER,
	"AMOUNT"	INTEGER,
	"TYPE"	TEXT,
    "DATE"	TEXT,
    "TOTAL" INTEGER,
	"CATEGORY"	TEXT,
	"REASON"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
    )'''
    cursor.execute(sql)
    print(" User Table created successfully........")
    conn.commit()


    sql = '''CREATE TABLE "CASH" (
	"Income"    INTEGER,
    "Expense"   INTEGER,
    "Sum"   INTEGER     
    )'''
    cursor.execute(sql)
    conn.commit()


    sql = '''INSERT INTO CASH (Income, Expense, Sum) VALUES (0, 0, 0)'''
    cursor.execute(sql)
    conn.commit()


    sql = ''' INSERT INTO USER_LOGIN (NAME,PASSWORD) VALUES (?, ?) '''
    cursor.execute(sql,(name.upper(),password.hexdigest()))
    print("Data saved in User Table created successfully........")
    conn.commit()


    conn.close()
    setup.destroy()
    import app

setup = Tk()

setup.title("ACCOUNT TRACKER : INSTALLATION")  
setup.iconbitmap('images//account.ico')
setup.geometry('600x700+450+75')      #width-height-x-cordinate-y-cordinate
setup.resizable(width=0, height=0)     #window resize == FALSE

img = PhotoImage(file="images//account.png")
panel = Label(setup, image=img)
panel.pack()
nameLabel = Label(setup, text="ACCOUNT TRACKER", bg="#2b292c", fg="white", relief=RIDGE, font=("times new roman",30,"bold"), pady=2, height=2).pack(fill=X)
nameLabel = Label(setup, text="ENTER NAME", fg="#2b292c",bd=0, relief=RIDGE, font=("times new roman",16,"bold"),height=2).pack(fill=X,pady=(10,0))
nameEntry = Entry(setup, bd=5,bg="white", justify="center", fg="#2b292c", relief=RIDGE, font=("times new roman",16,"bold"))
nameEntry.pack(fill=X,padx=40)
passwordLabel = Label(setup, text="ENTER PASSWORD", fg="#2b292c",bd=0, relief=RIDGE, font=("times new roman",16,"bold"),height=2).pack(fill=X,pady=(10,0))
passwordEntry = Entry(setup, bd=5,bg="white", justify="center", fg="#2b292c", relief=RIDGE, font=("times new roman",16,"bold"))
passwordEntry.pack(fill=X,padx=40)

btn = Button(setup, text="INSTALLATION", command=appSetUp, font=("times new roman",16,"bold"), fg="#2b292c", bg="#EF3E5B").pack(fill=X,padx=200,pady=30)

footer = Label(setup,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg="white" ,bg="#2b292c",border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)


setup.mainloop()