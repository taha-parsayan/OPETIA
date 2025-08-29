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
import fnmatch

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
""" GUI Element variables """
var_pet_path = ctk.StringVar()
var_pet_path.set("Path to vol0000.nii.gz, vol0001.nii.gz, ...")
var_output_path = ctk.StringVar()
var_output_path.set("Path to OPETIA_output folder")
var_MRI_reg_matrix_folder = ctk.StringVar()
var_MRI_reg_matrix_folder.set("Path to folder with registration matrix")
var_check_smooth = ctk.IntVar()
var_check_smooth.set(True)
var_smooth_FWHM = ctk.IntVar()
var_smooth_FWHM.set(5)
var_reg_type = ctk.StringVar()
var_reg_type.set("Rigid-body (rotation + translation)")

""" Other Global Variables """
registration_type = "Rigid"


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

def set_reg_matix_address():
    folder_path = get_address_folder()
    if os.path.exists(folder_path):
        var_MRI_reg_matrix_folder.set(folder_path)
    else:
        messagebox.showinfo("Error...", "Invalid folder path!")

def set_reg_type(choice):
    registration_type = linear_options_dict[choice]
  

# Image processing pipeline
def btn_process_data():
    
    t1 = time.time()

    print("\n")
    print("____________OPETIA is Processing your data___________")

    # Co-registering PET vols to T1
    # Here images still have the skull
    print("\n")
    print("Coregistering PET volumes to T1 space...")

    def find_PET_volumes(path):
        return sorted(fnmatch.filter(os.listdir(path), 'vol*.nii.gz'))

    pet_vols = find_PET_volumes(var_pet_path.get())
    n = len(pet_vols)
    print(f"{n} PET volumes were found.")

    try:
        # Coregister PET to T1
        for vol_names in pet_vols:
            input_image = os.path.join(var_pet_path.get(), f"{vol_names}")
            ref_image = os.path.join(var_pet_path.get(), "T1.nii.gz")
            output_name = vol_names.replace(".nii.gz", "") # So that I can add stuff to the sequel of the file name
            output_path = os.path.join(var_output_path.get(), f"{output_name}_coreg.nii.gz")
            ipf.co_registration(input_image, ref_image, output_path, registration_type)

        # Add coregistered vols to create PET.nii.gz
        ipf.add_PET_vols(var_output_path.get())


        print("Co-registration from PET to T1 space completed successfully.")
    except Exception as e:
        print(f"Error during Registration to MNI152 space:\n{e}")



    t2 = time.time()
    print("\nFinished processing.")
    print(f"Total time: {(t2-t1)/60:.2f} minutes")

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
# Frame 2: Co-registration type

frame2 = ctk.CTkFrame(master=app, width=390, height=75, border_color="#ffffff", border_width=1)
frame2.place(x=5, y=165)

lable3 = ctk.CTkLabel(master=frame2, text="Co-registration type (PET to T1):", font=("Times New Roman", 15))
lable3.place(x=5, y=5)

# Linear options mapping
linear_options_dict = {
    "Translation (shifts)": "Translation",
    "Rigid-body (rotation + translation)": "Rigid",
    "Rigid + uniform scaling": "Similarity",
    "Affine (rigid + scaling + shearing)": "Affine"
}

combobox1 = ctk.CTkComboBox(master=frame2, width=380, values=list(linear_options_dict.keys()),
                                variable=var_reg_type,
                                command=set_reg_type)
combobox1.place(x=5, y=35)

#------------------------------
# Frame 3: Registration matrix

frame3 = ctk.CTkFrame(master=app, width=390, height=70, border_color="#ffffff", border_width=1)
frame3.place(x=5, y=250)

lable4 = ctk.CTkLabel(master=frame3, text="Folder containing MRI native-to-MNI registration matrix:", font=("Times New Roman", 15))
lable4.place(x=5, y=5)

btn3 = ctk.CTkButton(master=frame3, text="Browse", width=100, height=25, command=set_reg_matix_address)
btn3.place(x=5, y=35)

entry3 = ctk.CTkEntry(master=frame3, textvariable=var_MRI_reg_matrix_folder, width = 265, height=25)
entry3.place(x=120, y=35)


# ---------------------------
# Frame4: smoothing
frame4 = ctk.CTkFrame(master=app, width=390, height=35, border_color="#ffffff", border_width=1)
frame4.place(x=5, y=330)

check2 = ctk.CTkCheckBox(master=frame4, text="Gaussian smoothing with FWHM of",
                        command = var_check_smooth,
                        variable=var_check_smooth, font=("Times New Roman", 15))
check2.place(x=5, y=5)

entry3 = ctk.CTkEntry(master=frame4, textvariable=var_smooth_FWHM, width = 40, height=25)
entry3.place(x=260, y=5)

lable5 = ctk.CTkLabel(master=frame4, text="mm", font=("Times New Roman", 15))
lable5.place(x=305, y=5)


#-------------------------------------
# Processing buttons

btn4 = ctk.CTkButton(master=app, text="Process data", width=390, height=25, command=btn_process_data)
btn4.place(x=5, y=370)

btn5 = ctk.CTkButton(master=app, text="Show registration result", width=390, height=25, command=btn_show_reg_result)
btn5.place(x=5, y=400)

btn6 = ctk.CTkButton(master=app, text="Show segmentation results", width=390, height=25, command=btn_show_seg_result)
btn6.place(x=5, y=430)

# Run the app
app.mainloop()