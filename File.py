from tkinter import *
import time
from VAD import *

ch=False
root= Tk()
root.geometry("350x300")
root.configure(background='#77CD88')
root.resizable(False, False)


myLable = Label(root,background='white' ,text="Hi! I'm gonna show you  \n"
                           "both voiced and unvoiced \n"
                           "parts of each audio.").grid(row=0, column=0,columnspan=4,padx=50,pady=10)


def plot():
    if clicked.get()!="choose audio" and clicked2.get()!="select a feature":
        str1="sentence"
        str1=str1+clicked.get()+".sp13.wav"
        print("ok")
        obj=myClass(str1,clicked2.get())
        obj.details()
        # myObject.showPlot()
        obj.showPlot()

def det():
    if clicked.get()!="choose audio" and clicked2.get()!="select a feature":
        str1="sentence"
        str1=str1+clicked.get()+".sp13.wav"
        obj=myClass(str1,clicked2.get())
        res=obj.details()

        print("Details:\n"+"fs : "+str(res['fs'])+"\n length of signal : "+str(res['length of signal']))
        myLable2 =Label(root,background='white',text="Details:\n"+"fs : "+str(res['fs'])+"\n length of signal : "+str(res['length of signal']),  borderwidth=2, relief="solid",width=20,height=5).grid(row=1, column=0,columnspan=4)
        obj.signalPlot()


clicked=StringVar()
clicked.set("choose audio")

clicked2=StringVar()
clicked2.set("select a feature")




drop = OptionMenu(root,clicked, "1","2","3", "4","5","6", "7","8","9","10").grid(row=2,column=0,columnspan=4,padx=50,pady=10)


drop2 = OptionMenu(root,clicked2,"Energy","ZCR").grid(row=4,column=0,columnspan=4,padx=50,pady=10)
# drop2.config(bg='#54ECDA')


btn = Button(root,background='#54ECDA',text="show a plot",command=plot).grid(row=5,column=0,columnspan=2,padx=50,pady=10)
btn2 = Button(root,background='#54ECDA',text="Details",command=det).grid(row=5,column=2,columnspan=2,padx=50,pady=10)

myLable2 = Label(root,background='white',text="Details:",  borderwidth=2, relief="solid",width=20,height=5).grid(row=1, column=0,columnspan=4)


root.mainloop()
