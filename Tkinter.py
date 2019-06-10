# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:33:06 2019

@author: siva1
"""

from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import time
import tkinter as tk

class UserInterface:
    def __init__(self, master):
        self.cancel_id = None
        
        self.Folderlbl = Label(window, text="Select the folder of the policies")
        self.Folderlbl.grid(column=0, row=0, sticky=W)
        self.Foldertxt = Entry(window,width=40)
        self.Foldertxt.grid(column=1, row=0, columnspan = 3)
        self.Floderbtn = Button(window, text="Browse Folder", command=self.clicked)
        self.Floderbtn.grid(column=4, row=0)


        self.Filelbl = Label(window, text="select if data need to generated for all the policies in folder")
        self.Filelbl.grid(column=0, row=1, sticky=W)
        self.FileSelected = IntVar()
        self.Filerad1 = Radiobutton(window,text='Yes', value=1, variable=self.FileSelected, command=self.FileClicked)
        self.Filerad2 = Radiobutton(window,text='No', value=2, variable=self.FileSelected, command=self.FileClicked)
        self.Filerad1.grid(column=1, row=1)
        self.Filerad2.grid(column=2, row=1)
        
        self.SelectFileslbl = Label(window, text="Select the files")
        self.SelectFileslbl.grid(column=0, row=2, sticky=W)
        self.SelectFilestxt = Entry(window,width=40)
        self.SelectFilestxt.grid(column=1, row=2, columnspan = 3)
        self.SelectFilesbtn = Button(window, text="Browse Files", command=self.SelectFilesclicked)
        self.SelectFilesbtn.grid(column=4, row=2)

        self.SetSelected = IntVar()
        self.rad1 = Radiobutton(window,text='Set1', value=1, variable=self.SetSelected)
        self.rad2 = Radiobutton(window,text='Set2', value=2, variable=self.SetSelected)
        self.rad3 = Radiobutton(window,text='Both', value=3, variable=self.SetSelected)
         
        self.lbl = Label(window, text="Select the set for which eml's need to be generated")
        self.lbl.grid(column = 0, row = 2, sticky=W)
        self.rad1.grid(column=1, row=3)
        self.rad2.grid(column=2, row=3)
        self.rad3.grid(column=3, row=3)
        
        self.Savelbl = Label(window, text="select if data need to generated for all the policies in folder")
        self.Savelbl.grid(column=0, row=4, sticky=W)
        self.SaveSelected = IntVar()
        self.Saverad1 = Radiobutton(window,text='Yes', value=1, variable=self.SaveSelected)
        self.Saverad2 = Radiobutton(window,text='No', value=2, variable=self.SaveSelected)
        self.Saverad1.grid(column=1, row=4)
        self.Saverad2.grid(column=2, row=4)

        self.ParameterFilelbl = Label(window, text="Select the parameter policy file")
        self.ParameterFilelbl.grid(column=0, row=5, sticky=W)
        self.ParameterFiletxt = Entry(window,width=40)
        self.ParameterFiletxt.grid(column=1, row=5, columnspan = 3)
        self.ParameterFilebtn = Button(window, text="Browse", command=self.ParameterClicked)
        self.ParameterFilebtn.grid(column=4, row=5)
        
        self.PrintTxt = scrolledtext.ScrolledText(window,width=60,height=10)
        self.PrintTxt.grid(column = 0, row = 6, columnspan = 4)

        self.startButton = Button(master,text='Start', command=self.start)
        self.startButton.grid(row=8, column=1)

        self.stopButton = Button(master, text='Stop', command=self.stop)
        self.stopButton.grid(row=8, column=2)
        
        self.closeButton = Button(master, text='Close', command=self.close)
        self.closeButton.grid(row=8, column=3)

    def clicked(self):
        self.Folder = filedialog.askdirectory()
        self.Foldertxt.insert(1, self.Folder)
    
    def SelectFilesclicked(self):
        self.PolicyFiles = filedialog.askopenfilenames()
        self.SelectFilestxt.insert(1, self.PolicyFiles)
    
    def FileClicked(self):
        if self.FileSelected.get() == 2:
            self.SelectFilestxt.configure(state = "disabled" )
            self.SelectFilesbtn.configure(state = "disabled")
        else:
            self.SelectFilestxt.configure(state = "normal" )
            self.SelectFilesbtn.configure(state = "normal")
    
    def SetSelected(self):
        pass

    def SaveSelected(self):
        pass
    
    def ParameterClicked(self):
        self.ParameterFile = filedialog.askopenfilename()
        self.ParameterFiletxt.insert(1, self.ParameterFile)
    
    def start(self):
        self.PrintTxt.configure(state = 'normal')
        if(self.cancel_id==None):
            self.count = 0
            self.counter()
            
    def counter(self):
#        self.textBox.delete("1.0", END)
        if (self.count < 100):
            self.count += 1
            self.PrintTxt.insert(END, str(self.count)+'\n\n')
            self.cancel_id = self.PrintTxt.after(1000, self.counter)
            self.PrintTxt.yview(tk.END)
            print(self.count)
    
    def stop(self):
        if self.cancel_id is not None:
            self.PrintTxt.after_cancel(self.cancel_id)
            quit()
            self.cancel_id = None
            
    
    def close(self):
        quit()
        window.destroy()


window = Tk()
window.title("Text Processing")
window.geometry('700x400')
UserInterface(window)
window.mainloop()


