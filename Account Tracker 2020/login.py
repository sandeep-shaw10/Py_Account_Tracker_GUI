from datetime import date
from tkinter import *
import hashlib
import sqlite3

password = "admin"

def loginValidate():
    global name
    name = passcode.get()
    name = hashlib.md5(name.encode())

    #SQL OPERATION
    conn = sqlite3.connect('accountDatabase.db')
    print("LOGIN ")

    cursor = conn.cursor()

    #SQL OPERATION
    sql =''' SELECT * FROM USER_LOGIN WHERE PASSWORD = ?'''

    name = name.hexdigest()

    cursor.execute(sql, (name,))
    check = cursor.fetchone()

    conn.commit()

    conn.close()

    if check != None:
        login.destroy()
        print("LOGGED IN SUCCESSFULLY")
        import app
    else:
        print("ACCESS DENIED")


login = Tk()

login.title("ACCOUNT TRACKER : LOGIN")  
login.iconbitmap('images//account.ico')
login.geometry('600x600+350+100')      #width-height-x-cordinate-y-cordinate
login.resizable(width=0, height=0)     #window resize == FALSE

img = PhotoImage(file="images//account.png")
panel = Label(login, image=img)
panel.pack()
name = Label(login, text="ACCOUNT TRACKER", bg="#2b292c", fg="white", relief=RIDGE, font=("times new roman",30,"bold"), pady=2, height=2).pack(fill=X)
passwordLabel = Label(login, text="ENTER PASSWORD", fg="#2b292c",bd=0, relief=RIDGE, font=("times new roman",20,"bold"),height=2).pack(fill=X,pady=(30,0))
passcode = Entry(login,text="ENTER PASSWORD", bd=5,bg="white", justify="center", fg="#2b292c", relief=RIDGE, font=("times new roman",20,"bold"))
passcode.pack(fill=X,padx=20)
btn = Button(login, text="LOGIN", command=loginValidate, font=("times new roman",16,"bold"), fg="#2b292c", bg="#EF3E5B").pack(fill=X,padx=200,pady=10)

footer = Label(login,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg="white" ,bg="#2b292c",border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)


login.mainloop()