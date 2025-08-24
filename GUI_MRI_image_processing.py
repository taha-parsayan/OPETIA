"""
Graphical User Interface (GUI) for MRI Image Processing using ANTsPy and CustomTkinter.
Author: Taha Parsayan
"""

#------------------------------
# Import Libraries
#------------------------------
import os
import numpy as np
import pandas as pd
import ants
import Image_Processing_Functions as ipf
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import tkinter as tk

#------------------------------
# GUI Setup
#------------------------------

# Set appearance and theme
ctk.set_appearance_mode("dark")  # modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # themes: "blue", "green", "dark-blue"

# Create the app window
app = ctk.CTk()  
app.title("OPETIA - MRI Image Processing")
app.geometry("400x600")  # width x height
app.resizable(False, False)


#------------------------------
# Global Variables
#------------------------------

var_T1_path = ctk.StringVar()
var_T1_path.set("Enter path to T1.nii.gz")
var_output_path = ctk.StringVar()
var_output_path.set("Enter path to output folder")
var_mri_modality = ctk.StringVar()
var_mri_modality.set("T1 weighted")

# -------------------------------
# Function to run when button is clicked
# -------------------------------

def get_address_file():
    file = filedialog.askopenfile(mode='r', filetypes=[("NIfTI files", "*.nii"), ("Compressed NIfTI files", "*.gz")])
    if file:
        return os.path.abspath(file.name)
    return None


def get_address_folder():
    return filedialog.askdirectory()


def get_MRI_address():
    address = get_address_file()
    if address:
        var_T1_path.set(address)
        T1_dir = os.path.dirname(address)
        output_address = os.path.join(T1_dir, "OPETIA_output")
        var_output_path.set(output_address)
    else:
        messagebox.showinfo("Error...", "Invalid file path!")

def set_output_address():
    address = get_address_folder()
    if address:
        var_output_path.set(address)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_modality(choice):
    if choice == "T1 weigted":
        mri_modality = "t1"
    elif choice == "T2 weighted":
        mri_modality = "t2"
    elif choice == "FLAIR":
        mri_modality = "flair"

#------------------------------
# GUI Elements
#------------------------------

frame1 = ctk.CTkFrame(master=app, width=390, height=150, border_color="#ffffff", border_width=1)
frame1.place(x=5, y=5)

lable1 = ctk.CTkLabel(master=frame1, text="Set T1.nii.gz image address:", font=("Times New Roman", 15))
lable1.place(x=5, y=5)

btn1 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=get_MRI_address)
btn1.place(x=5, y=40)

entry1 = ctk.CTkEntry(master=frame1, textvariable = var_T1_path, width = 265, height=25)
entry1.place(x=120, y=40)

lable2 = ctk.CTkLabel(master=frame1, text="Set output folder address:", font=("Times New Roman", 15))
lable2.place(x=5, y=75)

btn2 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=set_output_address)
btn2.place(x=5, y=110)

entry2 = ctk.CTkEntry(master=frame1, textvariable=var_output_path, width = 265, height=25)
entry2.place(x=120, y=110)


#-------------------------------------

frame2 = ctk.CTkFrame(master=app, width=390, height=45, border_color="#ffffff", border_width=1)
frame2.place(x=5, y=160)

lable3 = ctk.CTkLabel(master=frame2, text="MRI image modality:", font=("Times New Roman", 15))
lable3.place(x=5, y=5)

combobox1 = ctk.CTkComboBox(master=frame2, width=235, height=25,
                                     values=["T1 weigted", "T2 weighted", "FLAIR"],
                                     command=set_modality,
                                     variable=var_mri_modality)
combobox1.place(x=150, y=10)

# Run the app
app.mainloop()


