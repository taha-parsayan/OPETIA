from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import myfunctions
import webbrowser
import time
import threading
import subprocess
from tkinter import PhotoImage
from PIL import Image, ImageTk

root = Tk()
root.geometry("245x580+0+0")
root.resizable(False, False)
root.title("OPETIA")

# ___Commands    
def btn_nifti_organizer_command():
    os.system('python3 NIFTI_organizer.py')
    
def btn_stage1_command():
    os.system('python3 structural_process.py')

def btn_stage2_command():
    os.system('python3 pet_process.py')

def btn_stage3_command():
    os.system('python3 ROI_analysis.py')

# ___GUI
frame1 = Frame(root, relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=235, height=570)
height = 225; dist = 85

logo = Image.open('logo.png')
logo = logo.resize((200, 200))
logo = ImageTk.PhotoImage(logo)
Label(frame1, image=logo, bg="white", bd=4, relief='raised').place(x=7, y=5, width=215, height=215)
Button(frame1, text='NIFTI organizer', command=btn_nifti_organizer_command).place(x=5, y=height, width=220, height=80)
Button(frame1, text='Structural image pre-processing', command=btn_stage1_command).place(x=5, y=height + dist, width=220, height=80)
Button(frame1, text='PET image pre-processing', command=btn_stage2_command).place(x=5, y=height + dist*2, width=220, height=80)
Button(frame1, text='ROI analysis', command=btn_stage3_command).place(x=5, y=height + dist*3, width=220, height=80)

root.mainloop()
