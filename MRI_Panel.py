"""
MRI Image Processing Panel for OPETIA:

This pipeline applies standard MRI image processing.
The image can be T1, T2, or Flair.

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

#------------------------------
# Main class
#------------------------------

class MRIPanel:
    def __init__(self, parent):
        """Initialize the MRI panel inside a parent frame."""
        self.parent = parent
        self._setup_variables()
        self._build_gui()
        # Lets print something to start
        self.log("OPETIA is ready to analyze your data!")
        self.log("Analyze log will be printed here.")

        # Download MRIcroGL if not exists
        

    # -------------------------------
    # Variables
    # -------------------------------
    def _setup_variables(self):
        self.var_mri_path = ctk.StringVar(value="Path to T1 or T2 or Flair.nii.gz")
        self.var_output_path = ctk.StringVar(value="Path to OPETIA_output folder")
        self.var_mri_modality = ctk.StringVar(value="T1 weighted")
        self.var_reg_class = ctk.StringVar(value="Nonlinear")
        self.var_reg_type = ctk.StringVar(value="Symmetric normalization (nonlinear warp)")
        self.var_check_delete_outputs = ctk.BooleanVar(value=True)

        # Processing configs
        self.mri_modality = "t1"
        self.registration_type = "SyN"

        # Registration dictionaries
        self.linear_options_dict = {
            "Translation (shifts)": "Translation",
            "Rigid-body (rotation + translation)": "Rigid",
            "Rigid + uniform scaling": "Similarity",
            "Affine (rigid + scaling + shearing)": "Affine"
        }

        self.nonlinear_options_dict = {
            "Symmetric normalization (nonlinear warp)": "SyN",
            "Elastic deformation using SyN": "ElasticSyN",
            "Nonlinear deformation (no affine initialization)": "SyNOnly",
            "SyN using cross-correlation metric": "SyNCC",
            "SyN with rigid + affine initialization": "SyNRA",
            "More aggressive SyN (stronger warps)": "SyNAggro",
            "SyN optimized for b0-dMRI → T1 registration": "SyNabp"
        }

    # -------------------------------
    # GUI Layout
    # -------------------------------
    def _build_gui(self):
        """Build all widgets inside the parent frame."""

        # --------------------------------
        # Configure main grid (2 columns)
        self.parent.grid_columnconfigure(0, weight=1)  # left side expands
        self.parent.grid_columnconfigure(1, weight=0)  # right side fixed
        self.parent.grid_rowconfigure(99, weight=1)    # log box expands vertically

        # --------------------------------
        # Pipeline image (right side)
        pipeline_image_path = os.path.join(os.getcwd(), "Images", "MRI_proc_pipeline.png")
        if os.path.exists(pipeline_image_path):
            pipeline_image = Image.open(pipeline_image_path)
            w, h = pipeline_image.size
            scale = 0.5
            new_w, new_h = int(w * scale), int(h * scale)
            pipeline_image = pipeline_image.resize((new_w, new_h), Image.LANCZOS)
            ctk_image = ctk.CTkImage(dark_image=pipeline_image, size=(new_w, new_h))
            label_image = ctk.CTkLabel(master=self.parent, image=ctk_image, text="")
            label_image.grid(row=0, column=1, rowspan=10, sticky="ne", padx=5, pady=5)

        # --------------------------------
        # Frame1: Input paths
        frame1 = ctk.CTkFrame(master=self.parent, border_color="#ffffff", border_width=1)
        frame1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        frame1.grid_columnconfigure(1, weight=1) # Right side of the frame is exandable

        ctk.CTkLabel(frame1, text="Set T1.nii.gz image address:").grid(row=0, column=0, sticky="w", columnspan=2, padx=5, pady=5)
        ctk.CTkButton(frame1, text="Browse", command=self.set_MRI_address).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ctk.CTkEntry(frame1, textvariable=self.var_mri_path).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(frame1, text="Set output folder address:").grid(row=2, column=0, sticky="w", columnspan=2, padx=5, pady=5)
        ctk.CTkButton(frame1, text="Browse", command=self.set_output_address).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ctk.CTkEntry(frame1, textvariable=self.var_output_path).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # --------------------------------
        # Checkbox
        ctk.CTkCheckBox(
            master=self.parent,
            text="Delete previous outputs if exist",
            variable=self.var_check_delete_outputs,
            font=("Times New Roman", 15)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # --------------------------------
        # Frame2: MRI Modality
        frame2 = ctk.CTkFrame(master=self.parent, border_color="#ffffff", border_width=1)
        frame2.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        frame2.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame2, text="MRI image modality:", font=("Times New Roman", 15)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        combobox1 = ctk.CTkComboBox(frame2,
                                    values=["T1 weigted", "T2 weighted", "FLAIR"],
                                    command=self.set_modality,
                                    variable=self.var_mri_modality)
        combobox1.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # --------------------------------
        # Frame3: Registration options
        frame3 = ctk.CTkFrame(master=self.parent, border_color="#ffffff", border_width=1)
        frame3.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        frame3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame3, text="Select Registration Class:", font=("Times New Roman", 15)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        combobox2 = ctk.CTkComboBox(frame3,
                                    values=["Nonlinear", "Linear"],
                                    variable=self.var_reg_class,
                                    command=self.set_reg_combo_box_type)
        combobox2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(frame3, text="Select Registration Type:", font=("Times New Roman", 15)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combobox3 = ctk.CTkComboBox(frame3,
                                         values=list(self.nonlinear_options_dict.keys()),
                                         variable=self.var_reg_type,
                                         command=self.set_reg_type)
        self.combobox3.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        # --------------------------------
        # Processing buttons
        ctk.CTkButton(
            master=self.parent, text="Process data",
            command=lambda: threading.Thread(target=self.btn_process_data, daemon=True).start()
        ).grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        ctk.CTkButton(master=self.parent, text="Show registration result", command=self.btn_show_reg_result)\
            .grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(master=self.parent, text="Show segmentation results", command=self.btn_show_seg_result)\
            .grid(row=6, column=0, sticky="ew", padx=5, pady=5)

        # --------------------------------
        # Log box (console)
        self.print_box = ctk.CTkTextbox(master=self.parent)
        self.print_box.grid(row=99, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.print_box.configure(state="disabled")


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

    def set_MRI_address(self):
        address = self.get_address_file()
        self.var_mri_path.set(address)
        output_address = os.path.join(os.path.dirname(address), "OPETIA_output")
        self.var_output_path.set(output_address)

    def set_output_address(self):
        address = self.get_address_folder()
        self.var_output_path.set(address)

    def set_modality(self, choice):
        if choice == "T1 weigted":
            self.mri_modality = "t1"
        elif choice == "T2 weighted":
            self.mri_modality = "t2"
        elif choice == "FLAIR":
            self.mri_modality = "flair"

    def set_reg_combo_box_type(self, choice):
        if choice == "Linear":
            keys = list(self.linear_options_dict.keys())
        else:
            keys = list(self.nonlinear_options_dict.keys())
        self.combobox3.configure(values=keys)
        self.var_reg_type.set(keys[0])
        self.set_reg_type(self.var_reg_type.get())

    def set_reg_type(self, registration_type):
        if self.var_reg_class.get() == "Linear":
            self.registration_type = self.linear_options_dict.get(registration_type, "Affine")
        else:
            self.registration_type = self.nonlinear_options_dict.get(registration_type, "SyN")

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

        # Output folder
        if self.var_check_delete_outputs.get():
            if os.path.exists(self.var_output_path.get()):
                shutil.rmtree(self.var_output_path.get())
            os.makedirs(self.var_output_path.get(), exist_ok=True)
        else:
            os.makedirs(self.var_output_path.get(), exist_ok=True)

        # Skull stripping
        self.log("\nSkull stripping...")
        try:
            ipf.skull_strip(self.var_mri_path.get(),
                             os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain.nii.gz"),
                             os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_mask.nii.gz"),
                             self.mri_modality)
            self.log("Skull stripping completed successfully.")
        except Exception as e:
            self.log(f"Error during Skull Stripping:\n{e}")
            return

        # Segmentation
        self.log("\nGM, WM, CSF segmentation in native space...")
        try:
            input_image = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain.nii.gz")
            brain_mask = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_mask.nii.gz")
            output_seg = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_segmentation.nii.gz")
            ipf.tissue_segmentation(input_image, brain_mask, output_seg)
            ipf.split_tissues(input_image, self.mri_modality, output_seg, self.var_output_path.get(), False)
            self.log("Segmentation completed successfully.")
        except Exception as e:
            self.log(f"Error during tissue segmentation:\n{e}")
            return

        # Registration to MNI
        self.log("\nImage registration to MNI152 space...")
        try:
            input_image = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain.nii.gz")
            output_mni = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_MNI.nii.gz")
            ipf.register_to_MNI(input_image, output_mni, self.registration_type, True)
            self.log("Registration to MNI completed successfully.")
        except Exception as e:
            self.log(f"Error during Registration:\n{e}")
            return

        # Registration of segments to MNI space
        self.log("\nRegistration of image segments from native to MNI152 space...")
        input_image = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_segmentation.nii.gz")
        output_path = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_segmentation_MNI.nii.gz")
        MRI_MNI = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_MNI.nii.gz")
        if os.path.exists(os.path.join(self.var_output_path.get(), "native_to_mni_1Warp.nii.gz")):
            # Registration was nonlinear
            transform_list = [os.path.join(self.var_output_path.get(), "native_to_mni_1Warp.nii.gz"), os.path.join(self.var_output_path.get(), "native_to_mni_0GenericAffine.mat")]
        else:
            # Registration was linear
            transform_list = os.path.join(self.var_output_path.get(), "native_to_mni_0GenericAffine.mat")

        try:
            ipf.apply_transform_to_image(input_image, output_path, transform_list)
            ipf.split_tissues(MRI_MNI, self.mri_modality, output_path, self.var_output_path.get(), True)

            self.log("Registration of Image segments to MNI152 space completed successfully.")
        except Exception as e:
            self.log(f"Error during registration of image segments to MNI152 space:\n{e}")

        t2 = time.time()
        self.log(f"\nFinished processing. Total time: {(t2 - t1)/60:.2f} minutes")

    def btn_show_reg_result(self):
        try:
            mni_img_path = os.path.join(os.getcwd(), "Templates/MNI152_T1_2mm_brain.nii.gz")
            reg_img_path = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_MNI.nii.gz")
            ipf.plot_overlay(mni_img_path, reg_img_path, "Registration Result: MNI (background) and T1 (overlay)")
        except Exception as e:
            self.log(f"Error displaying registration result:\n{e}")
            return

    def btn_show_seg_result(self):
        try:
            seg_img_path = os.path.join(self.var_output_path.get(), f"{self.mri_modality}_brain_segmentation_MNI.nii.gz")
            ipf.plot_image(seg_img_path, "Tissue Segmentation Result in MNI space", is_segmented=True)
        except Exception as e:
            self.log(f"Error displaying segmentation result:\n{e}")
            return