"""
Graphical User Interface (GUI) for PET Image Processing using ANTsPy and CustomTkinter.
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
import time
import shutil
from PIL import Image

#------------------------------
# GUI Setup
#------------------------------

# Set appearance and theme
ctk.set_appearance_mode("dark")  # modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # themes: "blue", "green", "dark-blue"

# Create the app window
app = ctk.CTk()  
app.title("OPETIA - PET Image Processing")
app.geometry("970x475")  # width x height
app.resizable(False, False)

#------------------------------
# Global Variables
#------------------------------

var_pet_path = ctk.StringVar()
var_pet_path.set("Path to vol0000.nii.gz, vol0001.nii.gz, ...")
var_output_path = ctk.StringVar()
var_output_path.set("Path to OPETIA_output folder")
var_check_registrer_matrix_exists = ctk.IntVar()
var_check_registrer_matrix_exists.set(True)
var_MRI_reg_matrix_folder = ctk.StringVar()
var_MRI_reg_matrix_folder.set("Path to folder with registration matrix")

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

def set_PET_folder():
    folder_path = get_address_folder()
    if os.path.exists(folder_path):
        var_pet_path.set(folder_path)
        var_output_path.set(os.path.join(folder_path, "OPETIA_output"))
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_output_address():
    address = get_address_folder()
    if os.path.exists(address):
        var_output_path.set(address)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_reg_matix_address():
    folder_path = get_address_folder()
    if os.path.exists(folder_path):
        var_MRI_reg_matrix_folder.set(folder_path)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

#------------------------------
# GUI Elements
#------------------------------

# Frame1: input paths

frame1 = ctk.CTkFrame(master=app, width=390, height=150, border_color="#ffffff", border_width=1)
frame1.place(x=5, y=5)

lable1 = ctk.CTkLabel(master=frame1, text="Set folder containing the PET volume(s):", font=("Times New Roman", 15))
lable1.place(x=5, y=5)

btn1 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=set_PET_folder)
btn1.place(x=5, y=40)

entry1 = ctk.CTkEntry(master=frame1, textvariable = var_pet_path, width = 265, height=25)
entry1.place(x=120, y=40)

lable2 = ctk.CTkLabel(master=frame1, text="Set output folder address:", font=("Times New Roman", 15))
lable2.place(x=5, y=75)

btn2 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=set_output_address)
btn2.place(x=5, y=110)

entry2 = ctk.CTkEntry(master=frame1, textvariable=var_output_path, width = 265, height=25)
entry2.place(x=120, y=110)


#------------------------------
# Frame 2: Registration Options

frame2 = ctk.CTkFrame(master=app, width=390, height=150, border_color="#ffffff", border_width=1)
frame2.place(x=5, y=165)

check1 = ctk.CTkCheckBox(master=frame2, text="Subjec's MRI was registered to MNI152 using OPETIA", variable=var_check_registrer_matrix_exists, font=("Times New Roman", 15))
check1.place(x=5, y=5)

lable3 = ctk.CTkLabel(master=frame2, text="Folder containing MRI native-to-MNI matrix:", font=("Times New Roman", 15))
lable3.place(x=5, y=35)

btn3 = ctk.CTkButton(master=frame2, text="Browse", width=100, height=25, command=set_reg_matix_address)
btn3.place(x=5, y=65)

entry3 = ctk.CTkEntry(master=frame2, textvariable=var_MRI_reg_matrix_folder, width = 265, height=25)
entry3.place(x=120, y=65)

# Run the app
app.mainloop()