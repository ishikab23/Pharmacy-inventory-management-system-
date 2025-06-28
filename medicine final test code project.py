import os
import random
import datetime
from tabulate import tabulate
import mysql.connector

mycon=mysql.connector.connect(host='localhost', user='root', password='Riya2210', database='medicine')

mycur=mycon.cursor()

def Store():
    sql="Insert into stock(Batch_no,name,date_man,date_exp,quantity,sell,balance,cost_unit)values(%s,%s,%s,%s,%s,%s,%s,%s)"
    print('\nPLEASE PROVIDE THE REQUIRED INFORMATION\n')
    acc=int(input('\nENTER THE BATCH NUMBER:'))
    nm=input('\nENTER THE NAME OF THE MEDICINE WITH POWER:')
    dbs=input('\nENTER THE DATE OF MANUFACTURE(YYYY-MM-DD):')
    dacc=input('\nENTER THE DATE OF EXPIRY(YYYY-MM-DD):')
    quan=int(input('\nENTER THE QUANTITY OF THE IMPORTED MEDICINE:'))
    sell=0
    balance=quan
    cost=int(input('\nENTER THE COST OF THE IMPORTED MEDICINE PER UNIT:'))
    value=(acc,nm,dbs,dacc,quan,sell,balance,cost)
    try:
        mycur.execute(sql,value)
        print(nm, ' ADDED TO THE STOCK')
        mycon.commit()
    except BaseException as e:
        printIn(e)


def Search_by_Name():
    ph=input('\nENTER THE MEDICINE NAME TO SEARCH:')
    sql="Select Batch_no, name, date_man, date_exp, quantity, cost_unit from stock where name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print('BATCH NUMBER:\t',rec[0])
        print('MEDICINE NAME:\t',rec[1])
        print('DATE OF MANUFACTURE:\t',rec[2])
        print('DATE OF EXPIRY:\t',rec[3])
        print('QUANITTY STORED:\t',rec[4])
        print('UNIT PRICE:\t',rec[5])


def Cost_Update():
    sql="Update stock set cost_unit=%s where name=%s";
    ph=input('\nENTER THE MEDICINE NAME TO CHANGE COST:')
    addr=int(input('\nENTER THE NEW COST PER UNIT:'))
    value=(addr,ph)
    try:
        mycur.execute(sql,value)
        mycon.commit()
        print('NEW COST OF',ph,'IS Rs',addr)
    except:
        print('UNABLE TO CHANGE COST!!!!')


def Sell():
    sql="Update stock set sell=%s,balance=%s where name=%s";
    ph=input('\nENTER THE MEDICINE NAME TO SELL:')
    addr=int(input('\nENTER THE QUANTITY TO SELL:'))
    sql2='select quantity from STOCK where name=%s'
    value2=(ph,)
    mycur.execute(sql2,value2)
    rec=mycur.fetchone()
    if(addr>rec[0]):
        print('INSUFFICIENT STOCK IN HAND!!!!!!')
        return
    else:
        balance=rec[0]-addr
        value=(addr,balance,ph)
        try:
            mycur.execute(sql,value)
            mycon.commit()
            print(addr,'UNITS OF',ph,'SOLD')
            print(balance,'UNITS LEFT')
        except:
            print('UNABLE TO SELL MEDICINE!!!!')


def Available():
    ph=input('\nENTER THE MEDICINE NAME TO SEARCH:')
    sql="Select balance from stock where name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print(rec[0],'UNITS OF',ph,'IS AVAILABLE')
         

def Dispose():
    print("\n MEDICINES THAT HAVE EXPIRED TODAY")
    
    q1="select Batch_no,name,date_exp from stock where date_exp<=NOW()"
    mycur.execute(q1)
    col=mycur.fetchall()
    print(tabulate(col,headers=["Batch_no.","Medicine Name","Date of Expiry"], tablefmt='grid'))
    
    q2="insert into dispose(Batch_no,Name,date_exp,amount)select Batch_no,name,date_exp,cost_unit from stock where Batch_no=%s"   
    nm=list(input("PLEASE SELECT BATCH NUMBER TO DISPOSE MEDICINE: "))
    value=(nm)
    mycur.execute(q2,value)
    mycon.commit()
    print('BATCH',nm,"MEDICINE SUCCESSFULLY DISPOSED")
    
    q3="Delete from stock where Batch_no=%s"
    mycur.execute(q3,value)
    mycon.commit()


def Search_Dispose():
    ph=input('\nENTER THE DISPOSED MEDICINE NAME TO SEARCH:')
    sql="Select * from Dispose where Name=%s"
    value=(ph,)
    mycur.execute(sql,value)
    rec=mycur.fetchone()
    if(rec==None):
        print(ph,'IS NOT AVAILABLE')
    else:
        print('BATCH NUMBER:\t',rec[0])
        print('MEDICINE NAME:\t',rec[1])
        print('DATE OF EXPIRY:\t',rec[2])
        print('BALANCE AMOUNT:\t',rec[3])
        
def Display_Stock():
    from tabulate import tabulate 
    med = "Select * from stock"
    mycur.execute(med)
    result = mycur.fetchall()
    mycon.commit
    print(tabulate(result,headers=["Batch_no.","Medicine Name","Date of Manufacture","Date of Expiry","Quantity","Sold","Units Left","Amount per unit"], tablefmt='grid'))

def Display_diposedstock():
    from tabulate import tabulate 
    med = "Select* from dispose"
    mycur.execute(med)
    result = mycur.fetchall()
    mycon.commit
    print(tabulate(result,headers=["Batch_no.","Medicine Name","Date of Manufacture","Amount per unit"], tablefmt='grid'))


def Close():
    os.system('cls')
    print('\nTHANK YOU FOR USING THE APPLICATION')
    quit()




print('------------WELCOME TO PHARMACY INFORMATION MANAGEMENT SYSTEM-------------\n\n')
while(True):
    os.system('cls')
    print('\n\nPRESS 1 TO ADD A NEW MEDICINE')
    print('PRESS 2 TO SEARCH A MEDICINE BY NAME')
    
    print('PRESS 3 TO UPDATE MEDICINE COST')
    print('PRESS 4 TO SELL MEDICINE')
    print('PRESS 5 TO CHECK AVAILABILITY')
    print('PRESS 6 TO DISPOSE EXPIRED MEDICINE')
    print('PRESS 7 TO SEARCH EXPIRED MEDICINE BY NAME')
    print('PRESS 8 TO DISPLAY THE STOCK OF MEDICINES')
    print('PRESS 9 TO DISPLAY THE DISPOSED MEDICINES')
    print('PRESS 10 TO CLOSE THE APPLICATION')
    choice=int(input('ENTER YOUR CHOICE : '))
    if(choice==1):
        os.system('cls')
        Store()
    elif(choice==2):
        os.system('cls')
        Search_by_Name()
    
    elif(choice==3):
        os.system('cls')
        Cost_Update()
    elif(choice==4):
        os.system('cls')
        Sell()
    elif(choice==5):
        os.system('cls')
        Available()
    elif(choice==6):
        os.system('cls')
        Dispose()
    elif(choice==7):
        os.system('cls')
        Search_Dispose()
    elif(choice==8):
        os.system('cls')
        Display_Stock()
    elif(choice==9):
        os.system('cls')
        Display_diposedstock()
    else:
        os.system('cls')
        Close()
            
    
    
    
        
           
    
















