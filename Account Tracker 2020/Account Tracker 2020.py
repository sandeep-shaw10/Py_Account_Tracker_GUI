import os.path
import time
from tkinter import *

name="Py_Accounts_GUI1/accountDatabase.db"
path = ["C:","D:","E:"]

#Searching the file location
def find(name,path):

    if os.path.exists('accountDatabase.db')==True:
        return "yes"

    print("APP INSTALLING : PLEASE WAIT")
    '''for drive in path:
        for root, dirs, files in os.walk(drive):
            if name in files:
                print(i)
                return os.path.join(root, name)'''

search = find(name,path)

#If don't exist require app installation
if search == None:
    print("APP INSTALLATION")
    import setup
    sys.exit()
#Else login admin
else:
    print("Login")
    import login
    sys.exit()