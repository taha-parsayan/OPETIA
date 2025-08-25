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
import time
import shutil
#------------------------------
# GUI Setup
#------------------------------

# Set appearance and theme
ctk.set_appearance_mode("dark")  # modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # themes: "blue", "green", "dark-blue"

# Create the app window
app = ctk.CTk()  
app.title("OPETIA - MRI Image Processing")
app.geometry("800x600")  # width x height
app.resizable(False, False)


#------------------------------
# Global Variables
#------------------------------

""" GUI Elements Variables """

var_mri_path = ctk.StringVar()
var_mri_path.set("Enter path to T1.nii.gz")
var_output_path = ctk.StringVar()
var_output_path.set("Enter path to output folder")
var_mri_modality = ctk.StringVar()
var_mri_modality.set("T1 weighted")
var_reg_class = ctk.StringVar()
var_reg_class.set("Nonlinear")
var_reg_type = ctk.StringVar()
var_reg_type.set("Symmetric normalization (nonlinear warp)")
var_check_delete_outputs = ctk.BooleanVar()
var_check_delete_outputs.set(True)

""" Other Global Variables """
mri_modality = "t1"
registration_type = "SyN"

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

def set_MRI_address():
    address = get_address_file()
    if address:
        var_mri_path.set(address)
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

def set_reg_combo_box_type(choice):
    if choice == "Linear":
        keys = list(linear_options_dict.keys())
        combobox3.configure(values=keys)
        var_reg_type.set(keys[0])
        set_reg_type(var_reg_type.get())
    else:  # Nonlinear
        keys = list(nonlinear_options_dict.keys())
        combobox3.configure(values=keys)
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

    t1 = time.time()

    print("\n")
    print("____________OPETIA is Processing your data___________")

    # Output folder
    if var_check_delete_outputs.get():
        if  os.path.exists(var_output_path.get()):
            shutil.rmtree(var_output_path.get())
            os.makedirs(var_output_path.get())

        else:
            os.makedirs(var_output_path.get())
    else:
        if not os.path.exists(var_output_path.get()):
            os.makedirs(var_output_path.get())


    # Skull Stripping
    print("\n")
    print("Skull Stripping...")

    output_path = os.path.join(var_output_path.get(), f"{mri_modality}_brain.nii.gz")
    output_path_mask = os.path.join(var_output_path.get(), f"{mri_modality}_brain_mask.nii.gz")
    try:
        ipf.skull_strip(var_mri_path.get(), output_path, output_path_mask, mri_modality)
        print("Skull Stripping completed successfully.")
    except Exception as e:
        print(f"Error during Skull Stripping:\n{e}")

    # Tissue Segmentation
    print("\n")
    print("Tissue Segmentation in native space...")
    input_image = os.path.join(var_output_path.get(), f"{mri_modality}_brain.nii.gz")
    brain_mask = os.path.join(var_output_path.get(), f"{mri_modality}_brain_mask.nii.gz")
    output_path = os.path.join(var_output_path.get(), f"{mri_modality}_brain_segmentation.nii.gz")
    segmented_image = os.path.join(var_output_path.get(), f"{mri_modality}_brain_segmentation.nii.gz")
    try:
        ipf.tissue_segmentation(input_image, brain_mask, output_path)
        ipf.split_tissues(input_image, segmented_image, var_output_path.get(), False)

        print("Tissue Segmentation completed successfully.") 
    except Exception as e:
        print(f"Error during Tissue Segmentation:\n{e}")


    # Registration to MNI space
    print("\n")
    print("Image registration to MNI152 space...")
    input_image = os.path.join(var_output_path.get(), f"{mri_modality}_brain.nii.gz")
    output_path = os.path.join(var_output_path.get(), f"{mri_modality}_brain_MNI.nii.gz")
    try:
        ipf.register_to_MNI(input_image, output_path, registration_type)
        print("Registration to MNI152 space completed successfully.")
    except Exception as e:
        print(f"Error during Registration to MNI152 space:\n{e}")

    # Registration of segments to MNI space
    print("\n")
    print("Registration of image segments from native to MNI152 space...")
    input_image = os.path.join(var_output_path.get(), f"{mri_modality}_brain_segmentation.nii.gz")
    output_path = os.path.join(var_output_path.get(), f"{mri_modality}_brain_segmentation_MNI.nii.gz")
    transform_list = [os.path.join(var_output_path.get(), "native_to_mni_1Warp.nii.gz"), os.path.join(var_output_path.get(), "native_to_mni_0GenericAffine.mat")]
    MRI_MNI = os.path.join(var_output_path.get(), f"{mri_modality}_brain_MNI.nii.gz")

    try:
        ipf.apply_transform_to_image(input_image, output_path, transform_list)
        ipf.split_tissues(MRI_MNI, output_path, var_output_path.get(), True)

        print("Registration of Image segments to MNI152 space completed successfully.")
    except Exception as e:
        print(f"Error during Registration of Image segments to MNI152 space:\n{e}")



    t2 = time.time()
    print("\nFinished processing.")
    print(f"Total time: {(t2-t1)/60:.2f} minutes")


def btn_show_reg_result():
    try:
        mni_img_path = os.path.join(os.getcwd(), "Templates/MNI152_T1_2mm_brain.nii.gz")
        reg_img_path = os.path.join(var_output_path.get(), "T1_brain_MNI.nii.gz")
        ipf.plot_overlay(mni_img_path, reg_img_path, "Registration Result: MNI (background) and T1 (overlay)")
    except Exception as e:
        print(f"Error displaying registration result:\n{e}")

def btn_show_seg_result():
    try:
        seg_img_path = os.path.join(var_output_path.get(), "T1_brain_segmentation_MNI.nii.gz")
        ipf.plot_image(seg_img_path, "Tissue Segmentation Result in MNI space", is_segmented=True)
    except Exception as e:
        print(f"Error displaying segmentation result:\n{e}")

#------------------------------
# GUI Elements
#------------------------------

# Frame1: input paths

frame1 = ctk.CTkFrame(master=app, width=390, height=150, border_color="#ffffff", border_width=1)
frame1.place(x=5, y=5)

lable1 = ctk.CTkLabel(master=frame1, text="Set T1.nii.gz image address:", font=("Times New Roman", 15))
lable1.place(x=5, y=5)

btn1 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=set_MRI_address)
btn1.place(x=5, y=40)

entry1 = ctk.CTkEntry(master=frame1, textvariable = var_mri_path, width = 265, height=25)
entry1.place(x=120, y=40)

lable2 = ctk.CTkLabel(master=frame1, text="Set output folder address:", font=("Times New Roman", 15))
lable2.place(x=5, y=75)

btn2 = ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=set_output_address)
btn2.place(x=5, y=110)

entry2 = ctk.CTkEntry(master=frame1, textvariable=var_output_path, width = 265, height=25)
entry2.place(x=120, y=110)

#------------------------------------
# Check if preious outputs need to be deleted
check1 = ctk.CTkCheckBox(master=app, text="Delete previous outputs if exist", variable=var_check_delete_outputs, font=("Times New Roman", 15))
check1.place(x=10, y=160)
#-------------------------------------
# Frame2: MRI Modality Selection

frame2 = ctk.CTkFrame(master=app, width=390, height=45, border_color="#ffffff", border_width=1)
frame2.place(x=5, y=190)

lable3 = ctk.CTkLabel(master=frame2, text="MRI image modality:", font=("Times New Roman", 15))
lable3.place(x=5, y=5)

combobox1 = ctk.CTkComboBox(master=frame2, width=235, height=25,
                                     values=["T1 weigted", "T2 weighted", "FLAIR"],
                                     command=set_modality,
                                     variable=var_mri_modality)
combobox1.place(x=150, y=10)

#-------------------------------------
# Frame3: Registration Options
frame3 = ctk.CTkFrame(master=app, width=390, height=135, border_color="#ffffff", border_width=1)
frame3.place(x=5, y=240)

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

label4 = ctk.CTkLabel(master=frame3, text="Select Registration Class:", font=("Times New Roman", 15))
label4.place(x=5, y=5)

combobox2 = ctk.CTkComboBox(master=frame3, width=380, values=["Nonlinear", "Linear"],
                                 variable=var_reg_class,
                                 command=set_reg_combo_box_type)
combobox2.place(x=5, y=35)

label5 = ctk.CTkLabel(master=frame3, text="Select Registration Type:", font=("Times New Roman", 15))
label5.place(x=5, y=65)

combobox3 = ctk.CTkComboBox(master=frame3, width=380, values=list(nonlinear_options_dict.keys()),
                                variable=var_reg_type,
                                command=set_reg_type)
combobox3.place(x=5, y=95)

#-------------------------------------
# Processing buttons

btn3 = ctk.CTkButton(master=app, text="Process data", width=390, height=25, command=btn_process_data)
btn3.place(x=5, y=380)

btn4 = ctk.CTkButton(master=app, text="Show registration result", width=390, height=25, command=btn_show_reg_result)
btn4.place(x=5, y=410)

btn5 = ctk.CTkButton(master=app, text="Show segmentation results", width=390, height=25, command=btn_show_seg_result)
btn5.place(x=5, y=440)

# Run the app
app.mainloop()

