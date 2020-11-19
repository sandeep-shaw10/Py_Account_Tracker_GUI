#importing module
import tkinter.ttk                                                      #GUI
import tkinter as tk                                                    #''
from tkinter import *                                                   #''
import webbrowser                                                       #Browser Link
from datetime import date                                               #Date Time
import os                                                               #Operating System
import sqlite3                                                          #Database
import matplotlib.pyplot as plt                                         #Chart
from reportlab.pdfgen import canvas                                     #PDF Generation
from reportlab.lib import colors                                        #''
from reportlab.graphics.shapes import *                                 #''
from reportlab.graphics.charts.piecharts import Pie                     #''
from reportlab.graphics.charts.linecharts import HorizontalLineChart    #''
from reportlab.graphics.widgets.markers import makeMarker               #''
from reportlab.platypus import Table, TableStyle                        #''

#global variable declaration
'''Custom colour'''
col1 = "#EF3E5B"    #pinkish-red
col2 = "#ffffff"    #white
col3 = "#2b292c"    #dark-grey
global checkCash, checkAmt
checkCash = "BALANCED"
checkAmt = 0
global active1, active2, active3
active1 = active2 = active3 = False


#sql connection
conn = sqlite3.connect('accountDatabase.db')
cursor = conn.cursor()
sql ='''SELECT * FROM USER_LOGIN'''
cursor.execute(sql)
data = cursor.fetchall()
name = data[0][0]
conn.commit()


aboutMysite = "https://sandeep-shaw10.github.io/sightexplore/"
typeListIncome = [
    "HOME",
    "WORK",
    "SALARY"
]

typeListExpense = [
    "HOME",
    "WORK",
    "SALARY"
]
currentDate = date.today().strftime("%B %d, %Y")


#global function declaration
def maxVal(a,b):
    if a>b:
        return a
    else:
        return b

#check amt
def checknum(num1):
    num1 = list(num1)
    a = 0
    b = 0
    for i in range(len(num1)):
        if num1[i].isdigit() == True:
            a = a + 1
        elif num1[i] == ".":
            b = b + 1
        else:
            pass
    
    if (a+b)==len(num1) and b <= 1 :
        return True
    else:
        return False

#clear screen
def clear():
    _ = os.system('cls')    

#website linking
def openurl():
    webbrowser.open(aboutMysite, new=1)

#matplotlib chart
def graphAll():
    sql = "SELECT TOTAL, DATE FROM ACCOUNT_DATA"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    
    allData = []
    for i in range(len(data)):
        allData.append(data[i][0])
    
    allDate = []
    for i in range(1,len(data)+1):
        allDate.append(i)

    plt.close()

    # plotting the points  
    plt.plot(allDate, allData, 'ro')
    plt.plot(allDate, allData) 
    
    # naming the x axis 
    plt.xlabel('TRANSACTION') 
    # naming the y axis 
    plt.ylabel('TOTAL AMOUNT') 
    
    # giving a title to my graph 
    plt.title('ACCOUNT TRACKER : ALL TRANSACTION') 
    plt.legend()
    # function to show the plot 
    plt.show() 
    

def graphInc():
    sql = 'SELECT AMOUNT FROM ACCOUNT_DATA WHERE TYPE = "CREDIT"'
    cursor.execute(sql)
    data = cursor.fetchall()
    #print(data)
    
    allData = []
    for i in range(len(data)):
        allData.append(data[i][0])
    
    allDate = []
    for i in range(1,len(data)+1):
        allDate.append(i)

    plt.close()
    
    # plotting the points  
    plt.plot(allDate, allData, 'g^')
    plt.plot(allDate, allData) 
    
    # naming the x axis 
    plt.xlabel('TRANSACTION') 
    # naming the y axis 
    plt.ylabel('TOTAL AMOUNT') 
    
    # giving a title to my graph 
    plt.title('ACCOUNT TRACKER : INCOME TRANSACTION') 
    plt.legend()
    # function to show the plot 
    plt.show()

def graphExp():
    sql = 'SELECT AMOUNT FROM ACCOUNT_DATA WHERE TYPE = "DEBIT"'
    cursor.execute(sql)
    data = cursor.fetchall()
    #print(data)
    
    allData = []
    for i in range(len(data)):
        allData.append(data[i][0])
    
    allDate = []
    for i in range(1,len(data)+1):
        allDate.append(i)

    plt.close()
    
    # plotting the points  
    plt.plot(allDate, allData, 'bs')
    plt.plot(allDate, allData) 
    
    # naming the x axis 
    plt.xlabel('TRANSACTION') 
    # naming the y axis 
    plt.ylabel('TOTAL AMOUNT') 
    
    # giving a title to my graph 
    plt.title('ACCOUNT TRACKER : EXPENSE TRANSACTION') 
    plt.legend()
    # function to show the plot 
    plt.show()  

#GUI
root = Tk()
root.title("ACCOUNT TRACKER")           #Title
root.geometry('1260x700+0+0')           #Default dimension 16:9 Approx
root.iconbitmap('images//account.ico')          #icon

#SQL UPDATE
sql ='''SELECT * FROM CASH'''
global dataCount
cursor.execute(sql)
dataCount = cursor.fetchall()
balance = dataCount[0][2]
conn.commit()

balance = "Rs. "+str(balance)
allinc = " INCOME : "+str(dataCount[0][0])
allexp = "EXPENSE : "+str(dataCount[0][1])

sql ='''SELECT COUNT(*) FROM ACCOUNT_DATA WHERE TYPE = "CREDIT" '''
cursor.execute(sql)
data = cursor.fetchone()
#print(data)
countinc = " INCOME : " + str(data[0])
conn.commit()

if data[0] == 0:
    avgInc = 0.0
else:
    avgInc = round(dataCount[0][0]/data[0],2)   #Average Income

sql ='''SELECT COUNT(*) FROM ACCOUNT_DATA WHERE TYPE = "DEBIT" '''
cursor.execute(sql)
data = cursor.fetchone()
countexp = "EXPENSE : " + str(data[0])
conn.commit()

if data[0] == 0:
    avgExp = 0.0
else:
    avgExp = round(dataCount[0][1]/data[0],2)   #Average Expense

#print(avgInc," ",avgExp)

#function declaration
def addincome():
    global amt
    global cat
    global reason
    amt = entry11.get()
    reason = entry13.get()
    cat = defaultTypeListIn.get()
    if checknum(amt) == True and amt != "":
        #print(round(float(amt),2)," ",cat," ",reason)
        x = acc2['text']
        x = float(x[4:])
        #SQL OPERATION
        sql = '''INSERT INTO ACCOUNT_DATA (AMOUNT,TYPE,DATE,TOTAL,CATEGORY,REASON) VALUES (?,?,?,?,?,?) '''
        cursor.execute(sql,(round(float(amt),2),"CREDIT",currentDate,x+round(float(amt),2),cat,reason))
        print("INCOME CREDITED ",amt," on ",currentDate)
        conn.commit()
        sql = '''SELECT * FROM CASH'''
        cursor.execute(sql)
        data = cursor.fetchall()
        inc = float(data[0][0]) + (round(float(amt),2))
        expn = float(data[0][1])
        sum = inc - expn
        sql = '''DELETE FROM CASH'''
        cursor.execute(sql)
        conn.commit()
        sql = '''INSERT INTO CASH (Income, Expense, Sum) VALUES (?,?,?)'''
        cursor.execute(sql,(inc,expn,sum))
        conn.commit()
        acc2.config(text="Rs. "+str(sum))
        inSumLabel.config(text=" INCOME : "+str(inc))
        x = inTransLabel['text']
        x = x[10:]
        x = int(x)+1
        inTransLabel.config(text=" INCOME : "+str(x))
        avgIn.config(text=str(round((inc/x),2)))
    else:
        print("ERROR ",cat," ",reason)


def addexpense():
    global amt
    global cat
    global reason
    amt = entry21.get()
    reason = entry23.get()
    cat = defaultTypeListEx.get()
    if checknum(amt) == True and amt != "":
        #print(round(float(amt),2)," ",cat," ",reason)
        #SQL OPERATION
        sql = '''SELECT * FROM CASH'''
        cursor.execute(sql)
        data = cursor.fetchall()
        #print(data," ",type(data))
        #print(data[0]," ",type(data[0]))
        #print(data[0][1]," ",type(data[0][0]))   
        inc = float(data[0][0]) 
        expn = float(data[0][1])
        sum = float(data[0][2])

        if(round(float(amt),2) <= sum):
            sql = '''INSERT INTO ACCOUNT_DATA (AMOUNT,TYPE,DATE,TOTAL,CATEGORY,REASON) VALUES (?,?,?,?,?,?) '''
            cursor.execute(sql,(round(float(amt),2),"DEBIT",currentDate,sum-round(float(amt),2),cat,reason))
            print("EXPENSE DEBITED ",amt," on ",currentDate)
            conn.commit()

            expn = expn + (round(float(amt),2))
            sum = inc - expn
            sql = '''DELETE FROM CASH'''
            cursor.execute(sql)
            conn.commit()
            sql = '''INSERT INTO CASH (Income, Expense, Sum) VALUES (?,?,?)'''
            cursor.execute(sql,(inc,expn,sum))
            conn.commit()
            acc2.config(text="Rs. "+str(sum))
            exSumLabel.config(text="EXPENSE : "+str(expn))
            x = exTransLabel['text']
            x = x[10:]
            x = int(x)+1
            exTransLabel.config(text="EXPENSE : "+str(x))
            avgEx.config(text=str(round((expn/x),2)))    
        else:
            print("UNDERFLOW")
    else:
        print("ERROR ",cat," ",reason)


#frame definition
titleFrame = LabelFrame(root)
titleFrame.pack(fill=X)

dataFrame = LabelFrame(root, text=name.upper(), fg=col1,bg=col2,padx=5, pady=5)
dataFrame.pack(fill=X, padx=10)

inputFrame = LabelFrame(root, text="INCOME / EXPENDITURE", fg=col1, bg=col2, padx=5, pady=5)
inputFrame.pack(fill=X, padx=10)

visualFrame = LabelFrame(root, text="VIEW TRANSACTION", fg=col1, bg=col2, padx=5, pady=5)
visualFrame.pack(fill=X, padx=10)

calFrame = LabelFrame(root, text="CALCULATION", fg=col2, bg=col3, padx=5, pady=5)
calFrame.pack(fill=X, padx=10,pady=(20,0))

#sub-function
def cashLeft():
    hand = cashHand.get()
    if checknum(hand) == True and hand != "":
        check = acc2['text']
        check = check[4:]
        #print(check)
        difference = float(check) - float(hand)
        #print(difference)
        if difference == 0:
            checkCash = "BALANCED"
            checkAmt = 0
        elif difference > 0:
            checkCash = "RECESS"
            checkAmt = difference
        else:
            checkCash = "EXCESS"
            checkAmt = difference * (-1)
        #print(type(status))
        status.config(text=checkCash)
        amtstatus.config(text=str(checkAmt))
    else:
        print("ERROR")
        status.config(text="BALANCED")
        amtstatus.config(text="0")

def resetLast():
    sql = '''SELECT * FROM ACCOUNT_DATA ORDER BY ID DESC LIMIT 1'''
    cursor.execute(sql)
    data = cursor.fetchone()
    #print(data)
    #print(len(data))
    if len(data) != 0:
        id = data[0]
        amt = data[1]
        val = data[2]
        #print(amt," : ",val)
        conn.commit()

        sql = f'''DELETE FROM ACCOUNT_DATA WHERE ID = {id}'''
        cursor.execute(sql)
        conn.commit()

        sql = '''SELECT * FROM CASH'''
        cursor.execute(sql)
        dataCash = cursor.fetchone()
        conn.commit()

        income = dataCash[0]
        expense = dataCash[1]
        #print(dataCash)
        if val == "CREDIT":
            income -= amt
        else:
            expense -= amt
        sum = income - expense
        #print(income," ",expense," ",sum)

        sql = '''DELETE FROM CASH'''
        cursor.execute(sql)
        conn.commit()

        sql = '''INSERT INTO CASH (Income, Expense, Sum) VALUES (?,?,?)'''
        cursor.execute(sql,(income,expense,sum))
        conn.commit()

        #Configure update
        acc2.config(text="Rs. "+str(sum))
        inSumLabel.config(text=" INCOME : "+str(income))
        exSumLabel.config(text="EXPENSE : "+str(expense))
        if val == "CREDIT":
            x = inTransLabel['text']
            x = x[10:]
            x = int(x)-1
            inTransLabel.config(text=" INCOME : "+str(x))
            avgIn.config(text=str(round((income/x),2)))
        else:
            x = exTransLabel['text']
            x = x[10:]
            x = int(x)-1
            exTransLabel.config(text="EXPENSE : "+str(x))
            avgEx.config(text=str(round((expense/x),2))) 


def convertPdf():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")

    #---------------------PDF DETAIL-------------------------------------------
    documentFile = "myAccount"+dt_string+".pdf"
    xFile = documentFile
    #documentFile = "myAccount.pdf"
    documentTitle = "ACCOUNT TRACKER"
    title = "SANDEEP SHAW"
    subtitle = "ACCOUNT TRACKER"
    #-----------------------------------------------------

    
    pdf = canvas.Canvas(documentFile)
    pdf.setTitle(documentTitle)
    pdf.watermark = 'ACCOUNT TRACKER'

    #------------------------Reference--------------------------
    #pdf.drawString(100,810, 'x100')
    #pdf.drawString(200,810, 'x200')
    #pdf.drawString(300,810, 'x300')
    #pdf.drawString(400,810, 'x400')
    #pdf.drawString(500,810, 'x500')
    #pdf.drawString(10,100, 'y100')
    #pdf.drawString(10,200, 'y200')
    #pdf.drawString(10,300, 'y300')
    #pdf.drawString(10,400, 'y400')
    #pdf.drawString(10,500, 'y500')
    #pdf.drawString(10,600, 'y600')
    #pdf.drawString(10,700, 'y700')
    #pdf.drawString(10,800, 'y800')
    #---------------------------------------------------------------

    #SQL FETCH ------------------------------------------------------
    sql = "SELECT * FROM USER_LOGIN"
    cursor.execute(sql)
    userData = cursor.fetchone()

    sql = "SELECT * FROM CASH"
    cursor.execute(sql)
    cashData = cursor.fetchone()

    sql = "SELECT * FROM ACCOUNT_DATA"
    cursor.execute(sql)
    transData = cursor.fetchall()
    #print(transData)
    #print(userData,"\n",cashData,"\n",transData)

    conn.commit()
    #----------------------
    if transData != "":
        #PDF Content------------------------------------------------------------------------------
        pdf.setFillColorRGB(0.933, 0.242, 0.355)
        pdf.roundRect(25, 770, 550, 100, 5, stroke=1, fill=1)
        pdf.setFillColorRGB(0.976, 0.761, 0.761)
        pdf.roundRect(25, 660, 550, 100, 5, stroke=1, fill=1)
        pdf.roundRect(25, 555, 550, 100, 5, stroke=1, fill=1)
        pdf.roundRect(25, 450, 550, 100, 5, stroke=1, fill=1)
        pdf.setFillColorRGB(1,1,1)

        pdf.setFont('Helvetica-BoldOblique',36)
        pdf.drawCentredString(300,800,documentTitle)
        pdf.line(50,790,550,790)
        pdf.line(50,785,550,785)

        pdf.setFillColorRGB(0,0,0)
        pdf.setFont('Helvetica',18)
        pdf.drawString(50,735,f'    NAME :  {userData[0]}')
        pdf.drawString(50,705,f'    DATE :  {now.strftime("%d %B, %Y")}')
        pdf.drawString(50,675,f'     TIME :  {now.strftime("%H:%M:%S")}')
        

        pdf.drawString(50,630,f'TOTAL TRANSACTION :  {len(transData)}')
        x=y=0
        for i in range(len(transData)):
            if transData[i][2] == "DEBIT":
                x = x + 1
            else:
                y = y + 1
        pdf.drawString(50,600,f'          INCOME COUNT :  {x}')
        pdf.drawString(50,570,f'       EXPENSE COUNT :  {y}')


        pdf.drawString(50,525,f'            CURRENT BALANCE :  Rs. {cashData[2]}')
        pdf.drawString(50,495,f'  TOTAL INCOME ENTERED :  Rs. {cashData[0]}')
        pdf.drawString(50,465,f'TOTAL EXPENSE ENTERED :  Rs. {cashData[1]}')
        pdf.setFillColorRGB(0.933, 0.242, 0.355)
        pdf.setFont('Helvetica',28)
        pdf.drawString(150,400,'TRANSACTION CHART')
        pdf.setFillColorRGB(0,0,0)

        d = Drawing(200, 100)
        pc = Pie()
        pc.x = 65
        pc.y = 15
        pc.width = 70
        pc.height = 70
        pc.data = [x,y]
        pc.labels = ['CREDIT','DEBIT']
        pc.slices.strokeWidth=0.5
        pc.slices[0].popout = 10
        pc.slices[0].strokeWidth = 2
        pc.slices[0].strokeDashArray = [2,2]
        pc.slices[0].labelRadius = 1.75
        pc.slices[0].fontColor = colors.red
        d.add(pc)
        d.drawOn(pdf,380,560)

        d = Drawing(200, 100)
        pc = Pie()
        pc.x = 65
        pc.y = 15
        pc.width = 70
        pc.height = 70
        pc.data = [cashData[0],cashData[1]]
        pc.labels = ['INCOME','EXPENSE']
        pc.slices.strokeWidth=0.5
        pc.slices[0].popout = 10
        pc.slices[0].strokeWidth = 2
        pc.slices[0].strokeDashArray = [2,2]
        pc.slices[0].labelRadius = 1.75
        pc.slices[0].fontColor = colors.red
        d.add(pc)
        d.drawOn(pdf,380,455)

        d = Drawing(500, 300)
        data = []
        max = transData[i][0]
        for i in range(len(transData)):
            data.append(transData[i][4])
            if transData[i][4] >= max:
                max = transData[i][4]
        data = [tuple(data)]
        max = max + (10 - max%10)
        lc = HorizontalLineChart()
        lc.x = 50
        lc.y = 50
        lc.height = 300
        lc.width = 500
        lc.data = data
        lc.joinedLines = 1
        lc.categoryAxis.labels= "TOTAL TRANSACTION "
        lc.lines[0].symbol = makeMarker('FilledCircle')
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = max
        lc.valueAxis.valueStep = max/10
        lc.lines[0].strokeWidth = 2
        d.add(lc)
        d.drawOn(pdf,0,0)

        

        #----------------------------------------
        pdf.showPage()
        #---------------------------------------------------------------STARTING OF PAGE 2------------------------------------
        #Reference--------------------------
        #pdf.drawString(100,810, 'x100')
        #pdf.drawString(200,810, 'x200')
        #pdf.drawString(300,810, 'x300')
        #pdf.drawString(400,810, 'x400')
        #pdf.drawString(500,810, 'x500')
        #pdf.drawString(10,100, 'y100')
        #pdf.drawString(10,200, 'y200')
        #pdf.drawString(10,300, 'y300')
        #pdf.drawString(10,400, 'y400')
        #pdf.drawString(10,500, 'y500')
        #pdf.drawString(10,600, 'y600')
        #pdf.drawString(10,700, 'y700')
        #pdf.drawString(10,800, 'y800')
        #-----------------INCOME CHART---------------------------------------------    
        pdf.setFillColorRGB(0.933, 0.242, 0.355)
        pdf.setFont('Helvetica',28)
        pdf.drawString(90,800,'INCOME AND EXPENSE CHART')
        pdf.setFillColorRGB(0,0,0)

        d = Drawing(500, 300)
        data = []
        Indata = []
        Exdata = []
        sql = 'SELECT * FROM ACCOUNT_DATA WHERE TYPE = "CREDIT"'
        cursor.execute(sql)
        transData = cursor.fetchall()
        max1 = transData[0][1]
        for i in range(len(transData)):
            Indata.append(transData[i][1])
            if transData[i][1] >= max1:
                max1 = transData[i][1]
        sql = 'SELECT * FROM ACCOUNT_DATA WHERE TYPE = "DEBIT"'
        cursor.execute(sql)
        transData = cursor.fetchall()
        max2 = transData[0][1]
        for i in range(len(transData)):
            Exdata.append(transData[i][1])
            if transData[i][1] >= max2:
                max2 = transData[i][1]
        data = [tuple(Exdata),tuple(Indata)]
        lc = HorizontalLineChart()
        lc.x = 50
        lc.y = 50
        lc.height = 300
        lc.width = 500
        lc.data = data
        lc.joinedLines = 1
        lc.categoryAxis.labels= "TOTAL TRANSACTION "
        lc.valueAxis.valueMin = 0
        lc.lines[0].symbol = makeMarker('FilledCircle')
        lc.lines[1].symbol = makeMarker('Circle')
        lc.valueAxis.valueMax = maxVal(max1,max2)
        lc.valueAxis.valueStep = maxVal(max1,max2)/10
        lc.lines.strokeWidth = 2
        d.add(lc)
        d.drawOn(pdf,0,425)

        pdf.setFillColorRGB(1,0,0)
        pdf.roundRect(180, 440, 10, 10, 0, stroke=0, fill=1)
        pdf.setFillColorRGB(0,1,0)
        pdf.roundRect(380, 440, 10, 10, 0, stroke=0, fill=1)
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont('Helvetica-Bold',10)
        pdf.drawString(190,440,'EXPENSE')
        pdf.drawString(390,440,'INCOME')


        #----------------------TABLE------------------------------
        sql = 'SELECT ID, DATE, AMOUNT, TYPE, CATEGORY FROM ACCOUNT_DATA'
        cursor.execute(sql)
        transData = cursor.fetchall()
        heading = ('SL NO.','DATE','AMOUNT','TYPE','CATEGORY')
        transData.insert(0,heading)


        #--------------Arranging the Data----------------
        pdf.setFillColorRGB(0.933, 0.242, 0.355)
        pdf.setFont('Helvetica',28)
        pdf.drawString(150,400,'TRANSACTION TABLE')
        pdf.setFillColorRGB(0,0,0)

        printTab = []
        print(transData)
        if len(transData) <= 21:
            f = Table(transData)
            f.setStyle(TableStyle([('BACKGROUND',(0,0),(4,0),colors.pink),
                                    ('TEXTCOLOR',(0,0),(4,0),colors.red),
                                    ('ALIGNMENT',(0,0),(-1,-1),'CENTER'),
                                    ('LEFTPADDING',(0,0),(-1,-1),25),
                                    ('RIGHTPADDING',(0,0),(-1,-1),25),
                                ]))
            for i in range(1,len(transData)):
                if i%2!=0:
                    bgColor = colors.white
                else:
                    bgColor = colors.beige
                f.setStyle(TableStyle([('BACKGROUND',(0,i),(4,i),bgColor)]))
            f.wrapOn(pdf, 400, 400)
            f.drawOn(pdf, 35, 0)
        else:
            for i in range(22):
                printTab.append(transData[i])
            f = Table(printTab)
            print(printTab)
            f.setStyle(TableStyle([('BACKGROUND',(0,0),(4,0),colors.pink),
                                    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
                                    ('TEXTCOLOR',(0,0),(4,0),colors.red),
                                    ('ALIGNMENT',(0,0),(-1,-1),'CENTER'),
                                    ('LEFTPADDING',(0,0),(-1,-1),25),
                                    ('RIGHTPADDING',(0,0),(-1,-1),25),                                
                                ]))
            for i in range(1,22):
                if i%2!=0:
                    bgColor = colors.white
                else:
                    bgColor = colors.beige
                f.setStyle(TableStyle([('BACKGROUND',(0,i),(4,i),bgColor)]))
            f.wrapOn(pdf, 400, 400)
            f.drawOn(pdf, 35, 0)
            pdf.showPage()

            '''restricting area = 22  :::::::::::::  new page accomodation = 40'''
            count = len(transData) - 21
            recur = count // 47 + 1
            upfactor = 0
            for i in range (recur):
                printTab = []
                for j in range(47):
                    try:
                        printTab.append(transData[22 + i*47 + j])
                    except:
                        upfactor = 47 - j
                        break
                f = Table(printTab)
                f.setStyle(TableStyle([
                                        ('BACKGROUND',(0,0),(-1,-1),colors.beige),
                                        ('ALIGNMENT',(0,0),(-1,-1),'CENTER'),
                                        ('LEFTPADDING',(0,0),(-1,-1),30),
                                        ('RIGHTPADDING',(0,0),(-1,-1),30),
                                    ]))
                for k in range(len(printTab)):
                    if k%2!=0:
                        bgColor = colors.white
                    else:
                        bgColor = colors.beige
                    f.setStyle(TableStyle([('BACKGROUND',(0,k),(4,k),bgColor)]))
                f.wrapOn(pdf, 400, 400)
                f.drawOn(pdf, 40, (upfactor)*(845/(47)))
        pdf.showPage()

        #------------------DESIGN PAGE--------------------------------\
        pdf.setFillColorRGB(0.9,0.9,0.9)
        pdf.setFont("Helvetica",60)
        pdf.rotate(45)
        pdf.drawString(100,0,"ACCOUNT TRACKER")
        pdf.setFillColorRGB(0,0,0)

        #=============================================================




        

        #----------------------
        pdf.save()
    else:
        pass

#WINDOW-1 : ALL TRANSACTION DETAIL
def first1():
    global active1
    window1 = Tk()
    window1.title("ACCOUNT TRACKER : ALL TRANSACTION")           #Title
    window1.geometry('650x650+50+50')           #Default dimension 16:9 Approx
    window1.iconbitmap('images//account.ico')
    if active1 == False:
        active1 = True
        #SQL-OPERATION
        sql = '''SELECT DATE, TYPE, AMOUNT, CATEGORY, REASON FROM ACCOUNT_DATA'''
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.commit()
        #print(data)
        data.reverse()
        #Structure 1
        #----------------------------------------
        window1.configure(background=col1)
        heading = Label(window1, text="ACCOUNT TRACKER : ALL TRANSACTION", bd=12, relief=RIDGE, bg=col3 ,fg=col2 , font=("times new roman",20,"bold"), pady=2, height=2).pack(fill=X)
        subHead = LabelFrame(window1, fg=col1,bg=col2,padx=5, pady=5)
        subHead.pack(fill=X, padx=10, pady=20)
        subData1 = Label(subHead, text="DATE", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=0)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=1, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData1 = Label(subHead, text="TYPE", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=2)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=3, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData2 = Label(subHead, text="AMOUNT", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=4)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=5, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData3 = Label(subHead, text="CATEGORY", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=6)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=7, row=0, rowspan=4, sticky='ns', padx=20)
        subData4 = Label(subHead, text="REASON", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=8)
        #--------------------------------------------------------------
        main_frame = Frame(window1)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        for item in range(len(data)):
            Label(second_frame, text=data[item][0], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=0, pady=10, padx=10)
            Label(second_frame, text=data[item][1], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=1, pady=10, padx=75)
            Label(second_frame, text=data[item][2], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=2, pady=10, padx=70)
            Label(second_frame, text=data[item][3], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=3, pady=10, padx=70)
            if data[item][4] == '':
                Label(second_frame, text="- - - - - - -", font=("times new roman",16,"bold"), fg=col3,anchor='w').grid(row=item, column=4, pady=10, padx=(25,0))
            else:
                Label(second_frame, text=data[item][4], font=("times new roman",10,"bold"), fg=col3,anchor='w').grid(row=item, column=4, pady=10, padx=(25,0))

        #--------------------------------------------------------------
        footer = Label(window1,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg=col2 ,bg= col3,border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)
        #----------------------------------------
        window1.mainloop()
        active1 = False
    else:
        window1.destroy()
        active1 = False

#WINDOW-2 : ALL in-TRANSACTION DETAIL
def first2():
    global active2
    window2 = Tk()
    window2.title("ACCOUNT TRACKER : INCOME")           #Title
    window2.geometry('650x650+50+50')           #Default dimension 16:9 Approx
    window2.iconbitmap('images//account.ico')
    if active2 == False:
        active2 = True
        #SQL-OPERATION
        sql = '''SELECT DATE, AMOUNT, CATEGORY, REASON FROM ACCOUNT_DATA WHERE TYPE = "CREDIT" '''
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.commit()
        #print(data)
        data.reverse()
        #Structure 2
        #----------------------------------------
        window2.configure(background=col1)
        heading = Label(window2, text="ACCOUNT TRACKER : IN-TRANSACTION", bd=12, relief=RIDGE, bg=col3 ,fg=col2 , font=("times new roman",20,"bold"), pady=2, height=2).pack(fill=X)
        subHead = LabelFrame(window2, fg=col1,bg=col2,padx=5, pady=5)
        subHead.pack(fill=X, padx=10, pady=20)
        subData1 = Label(subHead, text="DATE", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=0)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=1, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData2 = Label(subHead, text="AMOUNT", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=2)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=3, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData3 = Label(subHead, text="CATEGORY", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=4)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=5, row=0, rowspan=4, sticky='ns', padx=20)
        subData4 = Label(subHead, text="REASON", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=6)
        #--------------------------------------------------------------
        main_frame = Frame(window2)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        for item in range(len(data)):
            Label(second_frame, text=data[item][0], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=0, pady=10, padx=10)
            Label(second_frame, text=data[item][1], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=1, pady=10, padx=70)
            Label(second_frame, text=data[item][2], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=2, pady=10, padx=70)
            if data[item][3] == '':
                Label(second_frame, text="- - - - - - -", font=("times new roman",16,"bold"), fg=col3,anchor='w').grid(row=item, column=3, pady=10, padx=(25,0))
            else:
                Label(second_frame, text=data[item][3], font=("times new roman",10,"bold"), fg=col3,anchor='w').grid(row=item, column=3, pady=10, padx=(25,0))
 
        #--------------------------------------------------------------
        footer = Label(window2,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg=col2 ,bg= col3,border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)
        #----------------------------------------
        window2.mainloop()
    else:
        window2.destroy()
        active2 = False


#WINDOW-3 : ALL out-TRANSACTION DETAIL
def first3():
    global active3
    window3 = Tk()
    window3.title("ACCOUNT TRACKER : EXPENDITURE ")           #Title
    window3.geometry('650x650+50+50')           #Default dimension 16:9 Approx
    window3.iconbitmap('images//account.ico')
    if active3 == False:
        active3 = True
        #SQL-OPERATION
        sql = '''SELECT DATE, AMOUNT, CATEGORY, REASON FROM ACCOUNT_DATA WHERE TYPE = "DEBIT" '''
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.commit()
        #print(data)
        data.reverse()
        #Structure 3
        #----------------------------------------
        window3.configure(background=col1)
        heading = Label(window3, text="ACCOUNT TRACKER : EX-TRANSACTION", bd=12, relief=RIDGE, bg=col3 ,fg=col2 , font=("times new roman",20,"bold"), pady=2, height=2).pack(fill=X)
        subHead = LabelFrame(window3, fg=col1,bg=col2,padx=5, pady=5)
        subHead.pack(fill=X, padx=10, pady=20)
        subData1 = Label(subHead, text="DATE", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=0)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=1, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData2 = Label(subHead, text="AMOUNT", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=2)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=3, row=0, rowspan=4, sticky='ns', padx=(20,0))
        subData3 = Label(subHead, text="CATEGORY", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=4)
        tkinter.ttk.Separator(subHead, orient=VERTICAL).grid(column=5, row=0, rowspan=4, sticky='ns', padx=20)
        subData4 = Label(subHead, text="REASON", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=6)
        #--------------------------------------------------------------
        main_frame = Frame(window3)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        for item in range(len(data)):
            Label(second_frame, text=data[item][0], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=0, pady=10, padx=10)
            Label(second_frame, text=data[item][1], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=1, pady=10, padx=70)
            Label(second_frame, text=data[item][2], font=("times new roman",16,"bold"), fg=col3).grid(row=item, column=2, pady=10, padx=70)
            if data[item][3] == '':
                Label(second_frame, text="- - - - - - -", font=("times new roman",16,"bold"), fg=col3 ,anchor='w').grid(row=item, column=3, pady=10, padx=(35,0))
            else:
                Label(second_frame, text=data[item][3], font=("times new roman",10,"bold"), fg=col3 ,anchor='w').grid(row=item, column=3, pady=10, padx=(35,0))
 
        #--------------------------------------------------------------
        footer = Label(window3,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg=col2 ,bg= col3,border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)
        #----------------------------------------
        window3.mainloop()
    else:
        window3.destroy()
        active3 = False

defaultTypeListIn = StringVar()
defaultTypeListIn.set(typeListIncome[0])

defaultTypeListEx = StringVar()
defaultTypeListEx.set(typeListExpense[0])

#layout name
heading = Label(titleFrame, text="ACCOUNT TRACKER", bd=12, relief=RIDGE, bg=col1 ,fg=col2 , font=("times new roman",30,"bold"), pady=2, height=2).pack(fill=X)

global acc2
#layout amount and name
acc1 = Label(dataFrame, text="AMOUNT : ", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=0)
acc2 = Label(dataFrame, text=balance, bd=5, relief=SUNKEN, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=20)
acc2.grid(row=0, column=1)
date1 = Label(dataFrame, text="DATE : ", bd=12, relief=FLAT, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=10).grid(row=0, column=2, padx=(125,0))
date2 = Label(dataFrame, text=currentDate , bd=5, relief=SUNKEN, fg=col1, bg=col2 , font=("times new roman",20,"bold"), pady=2, width=20).grid(row=0, column=3)
undo = Button(dataFrame, text="UNDO", command=resetLast, font=("times new roman",16,"bold"), fg=col2, bg=col1).grid(row=0, column=4, padx=(100,0))
about = Button(dataFrame, text="ABOUT", command=openurl, font=("times new roman",16,"bold"), fg=col2, bg=col1).grid(row=0, column=5, padx=(25,0))

#layout income
amt1 = Label(inputFrame, text="ENTER AMOUNT : ", bd=12, relief=FLAT, fg=col1 ,bg=col2, font=("times new roman",15,"bold"), pady=2, width=20).grid(row=0, column=0)
entry11 = Entry(inputFrame, bd=5, relief=SUNKEN, fg=col1 , font=("times new roman",15,"bold"), width=30)
entry11.grid(row=0, column=1)
type1 = Label(inputFrame, text="SELECT TYPE : ", bd=12, relief=FLAT, fg=col1 ,bg=col2, font=("times new roman",15,"bold"), pady=5, width=20).grid(row=1, column=0)
entry12 = OptionMenu(inputFrame, defaultTypeListIn, *typeListIncome)
entry12.grid(row=1, column=1)
reason1 = Label(inputFrame, text="REASON : ", bd=12, relief=FLAT, fg=col1 ,bg=col2, font=("times new roman",15,"bold"), pady=2, width=20).grid(row=2, column=0)
entry13 = Entry(inputFrame, bd=5, relief=SUNKEN, fg=col1 , font=("times new roman",15,"bold"), width=30)
entry13.grid(row=2, column=1)
btn1 = Button(inputFrame, text="ADD INCOME",relief=GROOVE , command=addincome, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=20).grid(row=3, column=1, pady=20)

#vertical line
tkinter.ttk.Separator(inputFrame, orient=VERTICAL).grid(column=2, row=0, rowspan=4, sticky='ns', padx=(40,0))

#layout expense
amt1 = Label(inputFrame, text="ENTER AMOUNT : ", bd=12, relief=FLAT, fg=col1, bg=col2, font=("times new roman",15,"bold"), pady=2, width=20).grid(row=0, column=3,padx=(20,5))
entry21 = Entry(inputFrame, bd=5, relief=SUNKEN, fg=col1 , font=("times new roman",15,"bold"), width=30)
entry21.grid(row=0, column=4)
type1 = Label(inputFrame, text="SELECT TYPE : ", bd=12, relief=FLAT, fg=col1 , font=("times new roman",15,"bold"), pady=5,bg=col2, width=20).grid(row=1, column=3,padx=(20,5))
entry22 = OptionMenu(inputFrame, defaultTypeListEx, *typeListExpense)
entry22.grid(row=1, column=4)
reason1 = Label(inputFrame, text="REASON : ", bd=12, relief=FLAT, fg=col1 ,bg=col2, font=("times new roman",15,"bold"), pady=2, width=20).grid(row=2, column=3,padx=(20,5))
entry23 = Entry(inputFrame, bd=5, relief=SUNKEN, fg=col1 , font=("times new roman",15,"bold"), width=30)
entry23.grid(row=2, column=4)
btn2 = Button(inputFrame, text="ADD EXPENSE",relief=GROOVE , command=addexpense, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=20).grid(row=3, column=4, pady=20)

#vertical line
tkinter.ttk.Separator(inputFrame, orient=VERTICAL).grid(column=5, row=0, rowspan=4, sticky='ns', padx=20)

global inSumLabel, exSumLabel
#transaction sum
totalSumLabel = Label(inputFrame, text="TRANSACTION AMOUNT", font=("times new roman",12,"bold"), fg=col1, bg=col2, width=25).grid(row=0,column=6)
inSumLabel = Label(inputFrame, text=allinc, font=("times new roman",12,"bold"), fg=col1, bg=col2, width=20)
inSumLabel.grid(row=1,column=6)
exSumLabel = Label(inputFrame, text=allexp, font=("times new roman",12,"bold"), fg=col1, bg=col2, width=20)
exSumLabel.grid(row=2,column=6)
dopdf = Button(inputFrame,text="SAVE PDF", relief=GROOVE, command=convertPdf, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=3, column=6, padx=10, pady=9)

#view transaction : all credit debit
transLabel = Label(visualFrame, text="TRANSACTION DETAIL", font=("times new roman",15,"bold"), fg=col1, bg=col2, width=30).grid(row=0,column=0,rowspan=3)
allbtn1 = Button(visualFrame, text="ALL", relief=GROOVE, command=first1, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=0, column=1, padx=10, pady=9)
inbtn1 = Button(visualFrame, text="CREDIT", relief=GROOVE, command=first2, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=1, column=1, padx=10, pady=9)
exbtn1 = Button(visualFrame, text="DEBIT", relief=GROOVE, command=first3, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=2, column=1, padx=10, pady=9)

#vertical line
tkinter.ttk.Separator(visualFrame, orient=VERTICAL).grid(column=2, row=0, rowspan=4, sticky='ns', padx=(80,40))

#view chart : all credit debit
graphLabel = Label(visualFrame, text="GRAPHICAL VISUALISATION", font=("times new roman",15,"bold"), fg=col1, bg=col2, width=30).grid(row=0,column=3,rowspan=3)
allbtn2 = Button(visualFrame, text="ALL", relief=GROOVE, command=graphAll, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=0, column=4, padx=10, pady=9)
inbtn2 = Button(visualFrame, text="CREDIT", relief=GROOVE, command=graphInc, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=1, column=4, padx=10, pady=9)
exbtn2 = Button(visualFrame, text="DEBIT", relief=GROOVE, command=graphExp, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=2, column=4, padx=10, pady=9)

#vertical line
tkinter.ttk.Separator(visualFrame, orient=VERTICAL).grid(column=5, row=0, rowspan=4, sticky='ns', padx=(80,40))

global inTransLabel, exTransLabel
totalTransLabel = Label(visualFrame, text="TRANSACTION COUNT", font=("times new roman",12,"bold"), fg=col1, bg=col2, width=20).grid(row=0,column=6)
inTransLabel = Label(visualFrame, text=countinc, font=("times new roman",12,"bold"), fg=col1, bg=col2, width=20)
inTransLabel.grid(row=1,column=6)
exTransLabel = Label(visualFrame, text=countexp, font=("times new roman",12,"bold"), fg=col1, bg=col2, width=20)
exTransLabel.grid(row=2,column=6)

#status
global status, amtstatus
status = Label(calFrame, text=checkCash, font=("times new roman",12,"bold"), fg=col2, bg=col3, width=20)
status.grid(row=0,column=4,padx=(5,1),pady=5, rowspan=2)
amtstatus = Label(calFrame, text=str(checkAmt), font=("times new roman",12,"bold"), fg=col2, bg=col3, width=20)
amtstatus.grid(row=0,column=5,padx=1,pady=5, rowspan=2)

#print(status)

#vertical line
tkinter.ttk.Separator(calFrame, orient=VERTICAL).grid(column=3, row=0, rowspan=4, sticky='ns', padx=(60,20))

#calcultion frame
Label1 = Label(calFrame,text="ENTER CASH IN HAND", font=("times new roman",12,"bold"), fg=col2, bg=col3, width=20).grid(row=0,column=0,padx=5,pady=5, rowspan=2)
cashHand = Entry(calFrame, bd=5, relief=SUNKEN, fg=col3 , font=("times new roman",11,"bold"), width=30)
cashHand.grid(row=0,column=1,padx=(0,5),pady=5, rowspan=2)
checkStatus =  Button(calFrame, text="CHECK", relief=GROOVE, command=cashLeft, font=("times new roman",15,"bold"), fg=col2, bg=col3, width=10).grid(row=0, column=2,padx=5 ,pady=5, rowspan=2)


#vertical line
tkinter.ttk.Separator(calFrame, orient=VERTICAL).grid(column=6, row=0, rowspan=4, sticky='ns', padx=(60,40))

#average
global avgIn, avgEx
avgInLabel = Label(calFrame, text="Average Income", font=("times new roman",10,"bold"), fg=col2, bg=col3, width=20).grid(row=0,column=7,padx=1)
avgExLabel = Label(calFrame, text="Average Expense", font=("times new roman",10,"bold"), fg=col2, bg=col3, width=20).grid(row=0,column=8,padx=1)
avgIn = Label(calFrame, text=str(avgInc), font=("times new roman",10,"bold"), fg=col2, bg=col3, width=20)
avgIn.grid(row=1,column=7,padx=1)
avgEx = Label(calFrame, text=str(avgExp), font=("times new roman",10,"bold"), fg=col2, bg=col3, width=20)
avgEx.grid(row=1,column=8,padx=1)

#footer
footer = Label(root,text="Made by Sandeep Shaw\t|\tv 1.0 2.11.2020\t|\t\u00A9 All right Reserved 2020",relief=GROOVE,fg=col3 ,bg= col1,border=0, font=("times new roman",10,"bold")).pack(side = BOTTOM, fill = X)

root.mainloop()

print("DATABASE: CONNECTION CLOSED")
print("APP CLOSED")
#clear()
conn.close()