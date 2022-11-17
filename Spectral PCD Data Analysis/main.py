from tkinter import *
import os
from tkinter import filedialog
import analyzeData
import hxtV3Read
import math
import numpy as np


window = Tk()
window.title("Main File")
# window.configure(width=500, height=300)

w1 = Frame(window)
w1.configure(width=1200, height=400)
# w1.geometry("1200x400")

w2 = Frame(window)
# w2.configure(width=1200, height=400)
# w2.geometry("800x400")

w1.pack(fill='both', expand=1)
w2.pack_forget()

label1 = Label(w1, text='Find the Two HEXITECH Files Below')
label1.config(font=('helvetica', 24))
label1.grid(row=0, column=0, columnspan=2, padx=30, pady=20)

label2 = Label(w1, text='Browse the Background File:')
label2.config(font=('helvetica', 18))
label2.grid(row=1, column=0, padx=30, pady=20)

label3 = Label(w1, text='Browse the Sample File:')
label3.config(font=('helvetica', 18))
label3.grid(row=1, column=1, padx=30, pady=20)

label11 = Label(w2, text='Input the Following Four Values')
label11.config(font=('helvetica', 24))
label11.grid(row=0, column=1, columnspan=2, padx=20, pady=20)

label12 = Label(w2, text='Bin Start:')
label12.config(font=('helvetica', 18))
label12.grid(row=1, column=0, padx=10, pady=10)

label13 = Label(w2, text='Bin End:')
label13.config(font=('helvetica', 18))
label13.grid(row=1, column=1, padx=10, pady=10)

label14 = Label(w2, text='Bin Width:')
label14.config(font=('helvetica', 18))
label14.grid(row=1, column=2, padx=10, pady=10)

label15 = Label(w2, text='Energy Window:')
label15.config(font=('helvetica', 18))
label15.grid(row=1, column=3, padx=10, pady=10)

label16 = Label(w2, text='Example: Bin Start = 30; Bin End = 45, Bin Width = 1; Energy Window = 5', fg='black')
label16.config(font=('helvetica', 18))
label16.grid(row=5, column=1, columnspan=2, pady=0)


def browseFiles():
    filename = filedialog.askopenfilename(title="Select a File", filetypes=[("Hexitech files", "*.hxt")])
    path1.configure(text="File Opened: " + filename)


path1 = Button(w1, text="Browse Files", command=browseFiles, wraplength=450, width=38, height=2)
path1.grid(row=2, column=0, pady=0)


def browseFiles2():
    filename = filedialog.askopenfilename(title="Select a File", filetypes=[("Hexitech files", "*.hxt")])
    path2.configure(text="File Opened: " + filename)


path2 = Button(w1, text="Browse Files", command=browseFiles2, wraplength=450, width=38, height=2)
path2.grid(row=2, column=1, pady=0)

entry11 = Entry(w2)
entry11.grid(row=2, column=0, padx=5, pady=10)

entry12 = Entry(w2)
entry12.grid(row=2, column=1, padx=5, pady=10)

entry13 = Entry(w2)
entry13.grid(row=2, column=2, padx=5, pady=10)

entry14 = Entry(w2)
entry14.grid(row=2, column=3, padx=5, pady=10)

def press():
    filePathB = path1.cget("text")[13:]
    filePathS = path2.cget("text")[13:]
    if filePathS == '' and filePathB == '':
        label1.config(text='Both are Empty', fg='red')
    elif filePathS == '':
        label1.config(text='Sample File is Empty', fg='red')
    elif filePathB == '':
        label1.config(text='Background File is Empty', fg='red')
    else:
        try:
            [data0, bins0] = hxtV3Read.hxtV3Read(filePathB)
            [data1, bins1] = hxtV3Read.hxtV3Read(filePathS)
            if data0.shape == (1,):
                if data0 == 0 and bins0 == 0 and data1 == 0 and bins1 == 0:
                    label1.config(text="Both Files Inputted aren't Hexitech Type. Please Check", fg='red')
                elif data0[0] == 0 and bins0[0] == 0:
                    label1.config(text="The Background File Inputted isn't Hexitech Type. Please Check", fg='red')
                elif data1[0] == 0 and bins1[0] == 0:
                    label1.config(text="The Sample File Inputted isn't Hexitech Type. Please Check", fg='red')
            else:
                w2.pack(fill='both', expand=1)
                w1.pack_forget()
        except FileNotFoundError:
            label1.config(text="File Inputted doesn't Exist. Please Check", fg='red')
        except:
            label1.config(text="File Paths aren't Correct. Please Check", fg='red')


Button(w1, text='Next', command=press, height=5, width=10).grid(row=3, column=0, columnspan=2, padx=20, pady=20)


def press2():
    binStart = entry11.get()
    binEnd = entry12.get()
    binWidth = entry13.get()
    energyWindow = entry14.get()
    filePathB = path1.cget("text")[13:]
    filePathS = path2.cget("text")[13:]
    if (binStart == '') + (binEnd == '') + (binWidth == '') + (energyWindow == '') > 1:
        label16.config(text='Multiple are Empty!', fg='red')
    elif binStart == '' or binEnd == '' or binWidth == '' or energyWindow == '':
        label16.config(text='One is Empty!', fg='red')
    else:
        try:
            if math.floor(float(binStart)) != math.ceil(float(binStart)) or math.floor(float(binEnd)) != \
                    math.ceil(float(binEnd)) or math.floor(float(binWidth)) != math.ceil(float(binWidth)) or \
                    math.floor(float(energyWindow)) != math.ceil(float(energyWindow)):
                label16.config(text='Inputs must be Integers!', fg='red')
            elif int(binEnd) < int(binStart):
                label16.config(text='The Bin End is less than the Start. Please Fix', fg='red')
            elif int(binEnd) - int(binStart) < float(binWidth):
                label16.config(text='The Bin Width is too big. Please Fix', fg='red')
            elif int(binEnd) - int(binStart) + 1 < float(energyWindow):
                label16.config(text='The Energy Window is too big. Please Fix', fg='red')
            else:
                try:
                    analyzeData.analyzeData(int(binStart), int(binEnd), int(binWidth), int(energyWindow), filePathB, filePathS)
                    window.destroy()
                except:
                    label16.config(text='Something went Wrong. Try Again', fg='red')
        except:
            label16.config(text='Check if all the inputs are Integers', fg='red')


Button(w2, text='Next', command=press2, height=5, width=10).grid(row=3, column=1, columnspan=2, padx=20, pady=10)
window.mainloop()
