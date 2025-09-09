"""
ROI Analysis Panel for OPETIA:

This pipeline segments both MRI and PET images into ROIs
and extracts volume, SUV, and SUVR for every region.

The output is saved as a .csv file.

Author: Taha Parsayan
"""

#------------------------------
# Import Libraries
#------------------------------
import os
import sys
import time
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import Image_Processing_Functions as ipf
import threading
import pandas as pd

# ------------------------------
# Main class
# ------------------------------

class ROIpanel:
    def __init__(self, parent):
        self.parent = parent
        self._setup_variables()
        self._build_gui()
        # Lets print something to start
        self.log("OPETIA is ready to analyze your data!")
        self.log("Analyze log will be printed here.")
    
    # -------------------------------
    # Variables
    # -------------------------------
    def _setup_variables(self):
        #----------------------------
        # GUI variables
        self.var_input_path = ctk.StringVar()
        self.var_input_path.set("Path to OPETIA_output folder")
        self.var_output_path = ctk.StringVar()
        self.var_output_path.set("Path to OPETIA_output/ROI_Analysis folder")
        self.var_SUVR_ref = ctk.StringVar()
        self.var_SUVR_ref.set("Cerebellum Gray Matter")
        self.var_atlas = ctk.StringVar()
        self.var_atlas.set("Harvard-Oxford Atlas")
        self.atlas_list = [
            "Harvard-Oxford Atlas"
        ]
        self.var_check_analyze_MRI = ctk.BooleanVar(value=True)
        self.var_check_analyze_PET = ctk.BooleanVar(value=True)

        #----------------------------
        # Other variables
        self.SUVR_ref = [
                    "Cerebellum",
                    "Cerebellum Gray Matter",
                    "Global Gray Matter",
                    "Global White Matter",
                    "Pons",
                    "Whole Brain"
                ]
        
        self.MRI_cortical_volume = pd.DataFrame(columns=["ROI", "volume"])
        self.MRI_subcortical_volume = pd.DataFrame(columns=["ROI", "volume"])

        self.all_measurements = pd.DataFrame(columns=["ROI", "volume"])

    # -------------------------------
    # GUI Layout
    # -------------------------------
    def _build_gui(self):
        
        # -------------------------------
        # Frame1: Input paths
        frame1 = ctk.CTkFrame(master=self.parent, width=390, height=150, border_color="#ffffff", border_width=1)
        frame1.place(x=5, y=5)

        ctk.CTkLabel(frame1, text="Set folder address containing processed images:").place(x=5, y=5)
        ctk.CTkButton(frame1, text="Browse", width=100, height=25, command=self.set_input_address).place(x=5, y=40)
        ctk.CTkEntry(frame1, textvariable=self.var_input_path, width=265, height=25).place(x=120, y=40)

        ctk.CTkLabel(frame1, text="Set output folder address:").place(x=5, y=75)
        ctk.CTkButton(frame1, text="Browse", width=100, height=25, command=self.set_output_address).place(x=5, y=110)
        ctk.CTkEntry(frame1, textvariable=self.var_output_path, width=265, height=25).place(x=120, y=110)

        # -------------------------------
        # Frame2: SUVR reference region
        frame2 = ctk.CTkFrame(master=self.parent, width=390, height=75, border_color="#ffffff", border_width=1)
        frame2.place(x=5, y=165)

        ctk.CTkLabel(frame2, text="Set the SUVR reference region:").place(x=5, y=5)
        ctk.CTkComboBox(frame2, width=380, height=25,
                            values=self.SUVR_ref,
                            variable=self.var_SUVR_ref,
                            ).place(x=5, y=40)
        
        # -------------------------------
        # Frame3: SUVR reference region
        frame3 = ctk.CTkFrame(master=self.parent, width=390, height=75, border_color="#ffffff", border_width=1)
        frame3.place(x=5, y=250)

        ctk.CTkLabel(frame3, text="Select the brain atlas:").place(x=5, y=5)
        ctk.CTkComboBox(frame3, width=380, height=25,
                            values=self.atlas_list,
                            variable=self.var_atlas,
                            ).place(x=5, y=40)
        
        # -------------------------------
        # Frame4: SUVR reference region
        frame4 = ctk.CTkFrame(master=self.parent, width=390, height=75, border_color="#ffffff", border_width=1)
        frame4.place(x=5, y=335)

        # Checkbox
        ctk.CTkCheckBox(master=frame4, text="Analyze MRI image", variable=self.var_check_analyze_MRI, font=("Times New Roman", 15)).place(x=10, y=10)
        ctk.CTkCheckBox(master=frame4, text="Analyze PET image", variable=self.var_check_analyze_PET, font=("Times New Roman", 15)).place(x=10, y=40)
        
        #-------------------------------------
        # Processing buttons

        ctk.CTkButton(master=self.parent, text="Process data", width=390, height=25, 
                             command=lambda: threading.Thread(target=self.btn_process_data, daemon=True).start()
                             ).place(x=5, y=415)
        
        # -------------------------------
        # Log box (console)
        self.print_box = ctk.CTkTextbox(master=self.parent, width=1010, height=300)
        self.print_box.place(x=5, y=480)
        self.print_box.configure(state="disabled")  # Start as read-only

    # -------------------------------
    # Functions
    # -------------------------------
    def get_address_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[("NIfTI files", "*.nii"), ("Compressed NIfTI files", "*.gz")])
        if file:
            return os.path.abspath(file.name)
        return None

    def get_address_folder(self):
        return filedialog.askdirectory()

    def set_input_address(self):
        address = self.get_address_folder()
        self.var_input_path.set(address)
        path = os.path.join(address, "ROI_Analysis")
        self.var_output_path.set(path)

    def set_output_address(self):
        address = self.get_address_folder()
        self.var_output_path.set(address)

        # For logging
    def log(self, message: str):
        """Print a message to the panel's log box."""
        self.print_box.configure(state="normal")
        self.print_box.insert("end", message + "\n")
        self.print_box.see("end")  # auto-scroll
        self.print_box.configure(state="disabled")

    # Processing methods
    def btn_process_data(self):
        t1 = time.time()
        self.log("\n____________OPETIA is Processing your data___________")

        # Create the output folder (delete if exists)
        if os.path.exists(self.var_input_path.get()):
            if os.path.exists(self.var_output_path.get()):
                shutil.rmtree(self.var_output_path.get()) # Remove ROI_Analysis folder
                os.makedirs(self.var_output_path.get()) # Create ROI_Analysis folder
                os.makedirs(os.path.join(self.var_output_path.get(), "MRI_Subcortical_ROIs")) # Create MRI_Subcortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "MRI_Cortical_ROIs")) # Create MRI_Cortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "PET_Subcortical_ROIs")) # Create PET_Subcortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "PET_Cortical_ROIs")) # Create PET_Cortical_ROIs folder
            else:
                os.makedirs(self.var_output_path.get()) # Create ROI_Analysis folder
                os.makedirs(os.path.join(self.var_output_path.get(), "MRI_Subcortical_ROIs")) # Create Subcortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "MRI_Cortical_ROIs")) # Create Cortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "PET_Subcortical_ROIs")) # Create PET_Subcortical_ROIs folder
                os.makedirs(os.path.join(self.var_output_path.get(), "PET_Cortical_ROIs")) # Create PET_Cortical_ROIs folder
        else:
            self.log("\nThe input path does not exists!")
            return
        
        # Segmenting the ROIs from MRI image
        if self.var_check_analyze_MRI.get():
            self.log("\nSegmentation of ROIs from the MRI image...")
            try:
                image = os.path.join(self.var_input_path.get(), "t1_GM_MNI.nii.gz")
                ipf.ROI_segmentation_Harvard_Oxford(
                    image,
                    self.var_output_path.get(),
                    "MRI")
                self.log("Image segmentation completed.")
            except Exception as e:
                self.log(f"\nError in ROI segmentation:\n{e}")

        # Segmenting the ROIs from PET image
        if self.var_check_analyze_PET.get():
            self.log("\nSegmentation of ROIs from the PET image...")
            try:
                image = os.path.join(self.var_input_path.get(), "pet_GM_MNI.nii.gz")
                ipf.ROI_segmentation_Harvard_Oxford(
                    image,
                    self.var_output_path.get(),
                    "PET")
                self.log("Image segmentation completed.")
            except Exception as e:
                self.log(f"\nError in ROI segmentation:\n{e}")

        # Calculate volume in mm3 from MRI
        self.log("\nCalculating volume in mm3 from MRI image...")

        if self.var_check_analyze_MRI.get():
            # Cortical
            try:
                dir = os.path.join(self.var_output_path.get(), "MRI_Cortical_ROIs")
                for i in range(1, 97): # 96 ROIs
                    image = os.path.join(dir, f"{str(i)}.nii.gz")
                    volume = ipf.calculate_mri_volume(image)
                    self.MRI_cortical_volume.loc[i-1, "volume"] = volume # i-1 because daframe index begins with 0
            except Exception as e:
                self.log(f"Error in calculating the volume from MRI image:\n{e}")
            # Subcortical
            try:
                dir = os.path.join(self.var_output_path.get(), "MRI_Subcortical_ROIs")
                for i in range(1, 20): #19 ROIs
                    image = os.path.join(dir, f"{str(i)}.nii.gz")
                    volume = ipf.calculate_mri_volume(image)
                    self.MRI_subcortical_volume.loc[i-1, "volume"] = volume # i-1 because daframe index begins with 0
            except Exception as e:
                self.log(f"Error in calculating the volume from MRI image:\n{e}")
            
            # Save
            current_dir = os.getcwd()
            dir = os.path.join(current_dir, "ROI_info") # Where ROI names are saved as txt
            path_cortical = os.path.join(dir, "Areas_Cortical.txt") # Cortical ROI names
            path_subcortical = os.path.join(dir, "Areas_Subcortical.txt") # Subcortical ROI names
            cortical_ROI_names = pd.read_csv(path_cortical, sep="\t", header=None)
            subcortical_ROI_names = pd.read_csv(path_subcortical, sep="\t", header=None)

            # Add ROI names to the dataframes
            self.MRI_cortical_volume["ROI"] = cortical_ROI_names
            self.MRI_subcortical_volume["ROI"] = subcortical_ROI_names

            # Concat cortical and subcortical as one row
            self.all_measurements = pd.concat([self.MRI_cortical_volume, self.MRI_subcortical_volume], ignore_index=True)

            path = os.path.join(self.var_output_path.get(), "MRI_measurements.csv")
            self.all_measurements.to_csv(path, sep="\t", index=True)

            self.log("Volume calculation completed successfully.")

        t2 = time.time()
        self.log(f"\nFinished processing. Total time: {(t2 - t1)/60:.2f} minutes")
