"""
OPETIA: Odense-Oxford PET Image Analysis
Author: Taha Parsayan
"""

#------------------------------
# Import Libraries
#------------------------------
import os
import time
import shutil
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image
import Image_Processing_Functions as ipf
from tkinter import PhotoImage
from MRI_Panel import MRIPanel
from PET_Panel import PETPanel
from ROI_Panel import ROIpanel

#------------------------------
# GUI Setup
#------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main window
app = ctk.CTk()
app.title("OPETIA")
# app.geometry("900x600")
app.state("zoomed") # Full screen
app.resizable(True, True)

# Set the taskbar icon (Windows)
current_dir = os.getcwd()
icon_png = os.path.join(current_dir, "Images", "Icon.png")   # PNG for Mac/Linux
icon_ico = os.path.join(current_dir, "Images", "Icon.ico")   # ICO for Windows
# Windows: .ico
if os.name == "nt" and os.path.exists(icon_ico):
    app.wm_iconbitmap(icon_ico)
# macOS/Linux: PNG
if os.path.exists(icon_png):
    icon_img = PhotoImage(file=icon_png)
    app.iconphoto(True, icon_img)
#------------------------------
# Functions
#------------------------------

def show_panel(panel_name):
    """Shows the selected panel on the right side."""
    for panel in panels.values():
        panel.pack_forget()   # hide all panels
    panels[panel_name].pack(fill="both", expand=True, padx=10, pady=10)

#------------------------------
# Layout: Left + Right
#------------------------------

# Left navigation panel
left_panel = ctk.CTkFrame(app, width=200, fg_color="white")
left_panel.pack(side="left", fill="y")

# Right content panel (container for switching content)
right_panel = ctk.CTkFrame(app, fg_color="black")
right_panel.pack(side="right", fill="both", expand=True)

#------------------------------
# Left Panel Content (Logo + Buttons)
#------------------------------

# Logo
current_dir = os.getcwd()
image_path = os.path.join(current_dir, "Images", "logo.png")
logo_img = Image.open(image_path)
w, h = logo_img.size
scale_factor = 0.18
new_w, new_h = int(w*scale_factor), int(h*scale_factor)
logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)
logo_img = ctk.CTkImage(dark_image=logo_img, size=(new_w, new_h))
logo_label = ctk.CTkLabel(master=left_panel, image=logo_img, text="")
logo_label.pack(padx=20, pady=20)

# Navigation buttons
btn1 = ctk.CTkButton(master=left_panel, text="MRI Image Processing", fg_color="black", command=lambda: show_panel("mri"))
btn1.pack(padx=10, pady=5)

btn2 = ctk.CTkButton(master=left_panel, text="PET Image Processing", fg_color="black", command=lambda: show_panel("pet"))
btn2.pack(padx=10,pady=5)

btn3 = ctk.CTkButton(master=left_panel, text="ROI Feature Extraction", fg_color="black", command=lambda: show_panel("roi"))
btn3.pack(padx=10,pady=5)

#------------------------------
# Right Panel Pages
#------------------------------

panels = {}

# MRI panel
panels["mri"] = ctk.CTkFrame(right_panel)
MRIPanel(panels["mri"])  

# PET panel
panels["pet"] = ctk.CTkFrame(right_panel)
PETPanel(panels["pet"]) 

# ROI panel
panels["roi"] = ctk.CTkFrame(right_panel)
ROIpanel(panels["roi"])
#------------------------------
# Start with MRI Panel
#------------------------------
show_panel("mri")

# Run
app.mainloop()
