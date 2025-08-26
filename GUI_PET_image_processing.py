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
app.geometry("970x535")  # width x height
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
var_reg_class = ctk.StringVar()
var_reg_class.set("Nonlinear")
var_reg_type = ctk.StringVar()
var_reg_type.set("Symmetric normalization (nonlinear warp)")
var_check_smooth = ctk.IntVar()
var_check_smooth.set(True)
var_smooth_FWHM = ctk.IntVar()
var_smooth_FWHM.set(5)

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
        var_MRI_reg_matrix_folder.set(var_output_path.get())
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_output_address():
    address = get_address_folder()
    if os.path.exists(address):
        var_output_path.set(address)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def check_reg():
    if var_check_registrer_matrix_exists.get():
        entry3.configure(state="normal")
        btn3.configure(state="normal")
        combobox1.configure(state="disabled")
        combobox2.configure(state="disabled")

    else:
        entry3.configure(state="disabled")
        btn3.configure(state="disabled")
        combobox1.configure(state="normal")
        combobox2.configure(state="normal")

def set_reg_matix_address():
    folder_path = get_address_folder()
    if os.path.exists(folder_path):
        var_MRI_reg_matrix_folder.set(folder_path)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_reg_combo_box_type(choice):
    if choice == "Linear":
        keys = list(linear_options_dict.keys())
        combobox2.configure(values=keys)
        var_reg_type.set(keys[0])
        set_reg_type(var_reg_type.get())
    else:  # Nonlinear
        keys = list(nonlinear_options_dict.keys())
        combobox2.configure(values=keys)
        var_reg_type.set(keys[0])
        set_reg_type(var_reg_type.get())

def set_reg_type(registration_type):
    registration_class = var_reg_class.get() # Linear or Nonlinear
    if registration_class == "Linear":
        registration_type = linear_options_dict[registration_type]
    else:  # Nonlinear
        registration_type = nonlinear_options_dict[registration_type]

# Image processing pipeline
def btn_process_data():
    pass

def btn_show_reg_result():
    pass

def btn_show_seg_result():
    pass
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
# If the subject's MRI was already registered to MNI152 using OPETIA
# then we apply the same transformation to the PET image.
# Otherwise we directly register the PET image to MNI152. 

frame2 = ctk.CTkFrame(master=app, width=390, height=225, border_color="#ffffff", border_width=1)
frame2.place(x=5, y=165)

check1 = ctk.CTkCheckBox(master=frame2, text="Subjec's MRI was registered to MNI152 using OPETIA",
                        command = check_reg,
                        variable=var_check_registrer_matrix_exists, font=("Times New Roman", 15))
check1.place(x=5, y=5)

lable3 = ctk.CTkLabel(master=frame2, text="Folder containing MRI native-to-MNI registration matrix:", font=("Times New Roman", 15))
lable3.place(x=5, y=35)

btn3 = ctk.CTkButton(master=frame2, text="Browse", width=100, height=25, command=set_reg_matix_address)
btn3.place(x=5, y=65)

entry3 = ctk.CTkEntry(master=frame2, textvariable=var_MRI_reg_matrix_folder, width = 265, height=25)
entry3.place(x=120, y=65)

# Linear options mapping
linear_options_dict = {
    "Translation (shifts)": "Translation",
    "Rigid-body (rotation + translation)": "Rigid",
    "Rigid + uniform scaling": "Similarity",
    "Affine (rigid + scaling + shearing)": "Affine"
}

# Nonlinear options mapping
nonlinear_options_dict = {
    "Symmetric normalization (nonlinear warp)": "SyN",
    "Elastic deformation using SyN": "ElasticSyN",
    "Nonlinear deformation (no affine initialization)": "SyNOnly",
    "SyN using cross-correlation metric": "SyNCC",
    "SyN with rigid + affine initialization": "SyNRA",
    "More aggressive SyN (stronger warps)": "SyNAggro",
    "SyN optimized for b0-dMRI → T1 registration": "SyNabp"
}

label4 = ctk.CTkLabel(master=frame2, text="Select Registration Class:", font=("Times New Roman", 15))
label4.place(x=5, y=95)

combobox1 = ctk.CTkComboBox(master=frame2, width=380, values=["Nonlinear", "Linear"],
                                 variable=var_reg_class,
                                 command=set_reg_combo_box_type)
combobox1.place(x=5, y=125)
combobox1.configure(state="disabled")

label5 = ctk.CTkLabel(master=frame2, text="Select Registration Type:", font=("Times New Roman", 15))
label5.place(x=5, y=155)

combobox2 = ctk.CTkComboBox(master=frame2, width=380, values=list(nonlinear_options_dict.keys()),
                                variable=var_reg_type,
                                command=set_reg_type)
combobox2.place(x=5, y=185)
combobox2.configure(state="disabled")


# ---------------------------
# Frame3: smoothing
frame3 = ctk.CTkFrame(master=app, width=390, height=35, border_color="#ffffff", border_width=1)
frame3.place(x=5, y=400)

check2 = ctk.CTkCheckBox(master=frame3, text="Gaussian smoothing with FWHM of",
                        command = check_reg,
                        variable=var_check_smooth, font=("Times New Roman", 15))
check2.place(x=5, y=5)

entry3 = ctk.CTkEntry(master=frame3, textvariable=var_smooth_FWHM, width = 40, height=25)
entry3.place(x=260, y=5)

label5 = ctk.CTkLabel(master=frame3, text="mm", font=("Times New Roman", 15))
label5.place(x=305, y=5)


#-------------------------------------
# Processing buttons

btn4 = ctk.CTkButton(master=app, text="Process data", width=390, height=25, command=btn_process_data)
btn4.place(x=5, y=440)

btn5 = ctk.CTkButton(master=app, text="Show registration result", width=390, height=25, command=btn_show_reg_result)
btn5.place(x=5, y=470)

btn6 = ctk.CTkButton(master=app, text="Show segmentation results", width=390, height=25, command=btn_show_seg_result)
btn6.place(x=5, y=500)

# Run the app
app.mainloop()