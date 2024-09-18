from Tkinter import *
import os
import ttk
import tkFileDialog
from tkFileDialog import askopenfile
import tkMessageBox as messagebox
import myfunctions
import webbrowser
import time
import threading


root = Tk()
root.geometry("245x280+500+250")
root.resizable(False, False)
root. title("OPETIA")


#___commands
def btn_stage1_command():
    os.system('python2 structural_process.py &')

def btn_stage2_command():
    os.system('python2 pet_process.py &')

def btn_stage3_command():
    os.system('python2 ROI_analysis.py &')

#___GUI
frame1 = Frame(root)
frame1.config(relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=235, height=270)


btn_stage1 = Button(frame1, text='Structural image pre-processing', command = btn_stage1_command).place(x=5,y=5, width=220, height = 80)
btn_stage2 = Button(frame1, text='PET image pre-processing', command = btn_stage2_command).place(x=5,y=90, width=220, height = 80)
btn_stage3 = Button(frame1, text='ROI analysis', command = btn_stage3_command).place(x=5,y=175, width=220, height = 80)

root.mainloop()
