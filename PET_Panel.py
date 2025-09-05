"""
PET Image Processing Panel for OPETIA
Author: Taha Parsayan
"""

# ------------------------------
# Import Libraries
# ------------------------------
import os
import sys
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import Image_Processing_Functions as ipf
import re
import threading

# ------------------------------
# Main class
# ------------------------------
class PETPanel:
    def __init__(self, parent):
        """Initialize the PET panel inside a parent frame."""
        self.parent = parent
        self._setup_variables()
        self._build_gui()

    # -------------------------------
    # Variables
    # -------------------------------
    def _setup_variables(self):
        self.var_pet_path = ctk.StringVar(value="Path to PET_dynamic.nii.gz")
        self.var_output_path = ctk.StringVar(value="Path to OPETIA_output folder")
        self.var_MRI_reg_matrix_folder = ctk.StringVar(value="Path to folder with registration matrix")
        self.var_MRI_masks_folder = ctk.StringVar(value="Path to folder with MRI masks")
        self.var_check_smooth = ctk.BooleanVar(value=True)
        self.var_smooth_FWHM = ctk.StringVar(value="5")
        self.var_reg_type = ctk.StringVar(value="Rigid-body (rotation + translation)")

        # Default config
        self.registration_type = "Rigid"
        self.linear_options_dict = {
            "Translation (shifts)": "Translation",
            "Rigid-body (rotation + translation)": "Rigid",
            "Rigid + uniform scaling": "Similarity",
            "Affine (rigid + scaling + shearing)": "Affine"
        }

    # -------------------------------
    # GUI Layout
    # -------------------------------
    def _build_gui(self):
        """Build all widgets inside the parent frame."""

        # Pipeline image
        pipeline_image_path = os.path.join(os.getcwd(), "Images", "PET_proc_pipeline.png")
        if os.path.exists(pipeline_image_path):
            pipeline_image = Image.open(pipeline_image_path)
            w, h = pipeline_image.size
            scale = 0.49
            new_w, new_h = int(w * scale), int(h * scale)
            pipeline_image = pipeline_image.resize((new_w, new_h), Image.LANCZOS)
            ctk_image = ctk.CTkImage(dark_image=pipeline_image, size=(new_w, new_h))
            label_image = ctk.CTkLabel(master=self.parent, image=ctk_image, text="")
            label_image.place(x=410, y=5)

        # -------------------------------
        # Frame1: Input path
        frame1 = ctk.CTkFrame(master=self.parent, width=390, height=150, border_color="#ffffff", border_width=1)
        frame1.place(x=5, y=5)

        ctk.CTkLabel(master=frame1, text="Set folder containing the PET volume(s):", font=("Times New Roman", 15)).place(x=5, y=5)
        ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=self.set_PET_folder).place(x=5, y=40)
        ctk.CTkEntry(master=frame1, textvariable = self.var_pet_path, width = 265, height=25).place(x=120, y=40)
        ctk.CTkLabel(master=frame1, text="Set output folder address:", font=("Times New Roman", 15)).place(x=5, y=75)
        ctk.CTkButton(master=frame1, text="Browse", width=100, height=25, command=self.set_output_address).place(x=5, y=110)
        ctk.CTkEntry(master=frame1, textvariable=self.var_output_path, width = 265, height=25).place(x=120, y=110)

        #------------------------------
        # Frame 2: Co-registration type

        frame2 = ctk.CTkFrame(master=self.parent, width=390, height=75, border_color="#ffffff", border_width=1)
        frame2.place(x=5, y=165)

        ctk.CTkLabel(master=frame2, text="Co-registration type (PET to T1):", font=("Times New Roman", 15)).place(x=5, y=5)
        ctk.CTkComboBox(master=frame2, width=380, values=list(self.linear_options_dict.keys()),
                                        variable=self.var_reg_type,
                                        command=self.set_reg_type).place(x=5, y=35)

        #------------------------------
        # Frame 3: Registration matrix

        frame3 = ctk.CTkFrame(master=self.parent, width=390, height=130, border_color="#ffffff", border_width=1)
        frame3.place(x=5, y=250)

        ctk.CTkLabel(master=frame3, text="Folder containing MRI brain masks:", font=("Times New Roman", 15)).place(x=5, y=5)
        ctk.CTkButton(master=frame3, text="Browse", width=100, height=25, command=self.set_brain_mask_address).place(x=5, y=35)
        ctk.CTkEntry(master=frame3, textvariable=self.var_MRI_masks_folder, width = 265, height=25).place(x=120, y=35)
        ctk.CTkLabel(master=frame3, text="Folder containing MRI native-to-MNI registration matrix:", font=("Times New Roman", 15)).place(x=5, y=65)
        ctk.CTkButton(master=frame3, text="Browse", width=100, height=25, command=self.set_reg_matrix_address).place(x=5, y=95)
        ctk.CTkEntry(master=frame3, textvariable=self.var_MRI_reg_matrix_folder, width = 265, height=25).place(x=120, y=95)

        # ---------------------------
        # Frame4: smoothing
        frame4 = ctk.CTkFrame(master=self.parent, width=390, height=35, border_color="#ffffff", border_width=1)
        frame4.place(x=5, y=390)

        ctk.CTkCheckBox(master=frame4, text="Gaussian smoothing with FWHM of",
                                command = self.var_check_smooth,
                                variable = self.var_check_smooth, font=("Times New Roman", 15)).place(x=5, y=5)
        ctk.CTkEntry(master=frame4, textvariable=self.var_smooth_FWHM, width = 40, height=25).place(x=260, y=5)
        ctk.CTkLabel(master=frame4, text="mm", font=("Times New Roman", 15)).place(x=305, y=5)

        #-------------------------------------
        # Processing buttons

        btn5 = ctk.CTkButton(master=self.parent, text="Process data", width=390, height=25, 
                             command=lambda: threading.Thread(target=self.btn_process_data, daemon=True).start()
                             ).place(x=5, y=430)
        btn6 = ctk.CTkButton(master=self.parent, text="Show registration result", width=390, height=25, command=self.btn_show_reg_result).place(x=5, y=460)
        btn7 = ctk.CTkButton(master=self.parent, text="Show segmentation results", width=390, height=25, command=self.btn_show_seg_result).place(x=5, y=490)

        # -------------------------------
        # Log box (console)
        self.log_box = ctk.CTkTextbox(master=self.parent, width=1090, height=250)
        self.log_box.place(x=5, y=530)
        self.log_box.configure(state="disabled")  # Start as read-only
        sys.stdout = StdoutRedirector(self.log_box)

    # -------------------------------
    # File selection methods
    # -------------------------------
    def get_address_file(self):
        file = filedialog.askopenfile(mode='r', filetypes=[("NIfTI files", "*.nii"), ("Compressed NIfTI files", "*.gz")])
        if file:
            return os.path.abspath(file.name)
        return None

    def get_address_folder(self):
        return filedialog.askdirectory()

    def set_PET_folder(self):
        pet_path = self.get_address_file()
        if pet_path and os.path.exists(pet_path):
            self.var_pet_path.set(pet_path)
            dir_path = os.path.dirname(pet_path)
            self.var_output_path.set(os.path.join(dir_path, "OPETIA_output"))
            self.var_MRI_reg_matrix_folder.set(self.var_output_path.get())
            self.var_MRI_masks_folder.set(self.var_output_path.get())
        else:
            messagebox.showinfo("Error...", "Invalid PET file path!")

    def set_output_address(self):
        address = self.get_address_folder()
        if os.path.exists(address):
            self.var_output_path.set(address)
        else:
            messagebox.showinfo("Error...", "Invalid folder path!")

    def set_reg_matrix_address(self):
        folder_path = self.get_address_folder()
        if os.path.exists(folder_path):
            self.var_MRI_reg_matrix_folder.set(folder_path)
        else:
            messagebox.showinfo("Error...", "Invalid folder path!")

    def set_brain_mask_address(self):
        path = self.get_address_file()
        if path:
            self.var_MRI_masks_folder.set(path)

    def set_reg_type(self, choice):
        self.registration_type = self.linear_options_dict.get(choice, "Rigid")

    # -------------------------------
    # Processing methods
    # -------------------------------
    def btn_process_data(self):
        t1 = time.time()
        print("\n____________OPETIA is Processing your data___________")

        # First need to split the dynamic PET into volumes
        print("\nSplitting the dynamic PET into its volumes...")

        input_PET_dynamic = self.var_pet_path.get()
        output_dir = self.var_output_path.get()
        try:
            ipf.split_dynamic_pet(input_PET_dynamic, output_dir)
            print("Dynamic PET volume splitting completed successfully.")
        except Exception as e:
            print(f"Error during splitting the dynamic PET:\n{e}")
            return
        
        # Co-registering PET vols to T1
        # Here images still have the skull
        print("\nCoregistering PET volumes to T1 space...")

        # Read the volumes
        def find_PET_volumes(path):
            """
            Find only PET volumes with names like vol0000.nii.gz, vol0001.nii.gz, etc.
            Ignores files like vol0000_coreg.nii.gz.
            """
            pattern = re.compile(r"^vol\d{4}\.nii\.gz$")  # exactly vol + 4 digits + .nii.gz
            return sorted([f for f in os.listdir(path) if pattern.match(f)])

        pet_vols = find_PET_volumes(self.var_output_path.get())
        n = len(pet_vols)
        print(f"{n} PET volumes were found.")

        try:
            # Coregister PET to T1
            for vol_names in pet_vols:
                input_image = os.path.join(self.var_output_path.get(), f"{vol_names}")
                dir = os.path.dirname(self.var_pet_path.get()) # Where T1.nii.gz is located
                ref_image = os.path.join(dir, "T1.nii.gz")
                output_name = vol_names.replace(".nii.gz", "") # So that I can add stuff to the sequel of the file name
                output_path = os.path.join(self.var_output_path.get(), f"{output_name}_coreg.nii.gz")
                ipf.co_registration(input_image, ref_image, output_path, self.registration_type)

            # Add coregistered vols to create PET.nii.gz
            ipf.add_PET_vols(self.var_output_path.get())

            print("Co-registration from PET to T1 space completed successfully.")
        except Exception as e:
            print(f"Error during co-registration to MNI152 space:\n{e}")
            return

        # Brain extraction
        print("\nSkull stripping...")
        input_image = os.path.join(self.var_output_path.get(), "pet_coreg.nii.gz")
        input_mask_folder = self.var_MRI_masks_folder.get()
        input_mask = os.path.join(input_mask_folder, "t1_brain_mask.nii.gz")
        output_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain.nii.gz")
        try:
            ipf.apply_mask(input_image, input_mask, output_image)
            print("Skull stripping completed successfully.")
        except Exception as e:
            print(f"Error during skull stripping:\n{e}")
            return

        # Smoothing the image in native space
        print("\nSmoothing the image in native space...")
        input_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain.nii.gz")
        output_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain_smooth.nii.gz")
        fwhm = self.var_smooth_FWHM.get()
        try:
            ipf.smooth_image(input_image, output_image, fwhm)
            print("Smoothing completed successfully.")
        except Exception as e:
            print(f"Error during smoothing in native space:\n{e}")
            return

        # Tissue Segmentation
        print("\nGM, WM, CSF segmentation in native space...")
        input_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain_smooth.nii.gz")
        input_mask_GM = os.path.join(self.var_MRI_masks_folder.get(), "Mask_t1_GM_native.nii.gz")
        input_mask_WM = os.path.join(vself.ar_MRI_masks_folder.get(), "Mask_t1_WM_native.nii.gz")
        input_mask_CSF = os.path.join(self.var_MRI_masks_folder.get(), "Mask_t1_CSF_native.nii.gz")
        output_GM = os.path.join(self.var_output_path.get(), "pet_GM_native.nii.gz")
        output_WM = os.path.join(self.var_output_path.get(), "pet_WM_native.nii.gz")
        output_CSF = os.path.join(self.var_output_path.get(), "pet_CSF_native.nii.gz")

        try:
            ipf.apply_mask(input_image, input_mask_GM, output_GM)
            ipf.apply_mask(input_image, input_mask_WM, output_WM)
            ipf.apply_mask(input_image, input_mask_CSF, output_CSF)
            print("Segmentation completed successfully.") 
        except Exception as e:
            print(f"Error during PET segmentation:\n{e}")
            return

        # Registration to MNI
        print("\n")
        print("Image registration to MNI152 space...")
        input_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain.nii.gz")
        output_path = os.path.join(self.var_output_path.get(), "pet_coreg_brain_MNI.nii.gz")

        if os.path.exists(os.path.join(self.var_output_path.get(), "native_to_mni_1Warp.nii.gz")):
            # Registration was nonlinear
            transform_list = [os.path.join(self.var_output_path.get(), "native_to_mni_1Warp.nii.gz"), os.path.join(self.var_output_path.get(), "native_to_mni_0GenericAffine.mat")]
        else:
            # Registration was linear
            transform_list = os.path.join(self.var_output_path.get(), "native_to_mni_0GenericAffine.mat")

        try:
            ipf.apply_transform_to_image(input_image, output_path, transform_list)
            print("Registration of Image to MNI152 space completed successfully.")
        except Exception as e:
            print(f"Error during registration of image to MNI152 space:\n{e}")
            return

        # Smoothing the image in MNI space
        print("\nSmoothing the image in MNI152 space...")
        input_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain_MNI.nii.gz")
        output_image = os.path.join(self.var_output_path.get(), "pet_coreg_brain_MNI_smooth.nii.gz")
        fwhm = self.var_smooth_FWHM.get()
        try:
            ipf.smooth_image(input_image, output_image, fwhm)
            print("Smoothing completed successfully.")
        except Exception as e:
            print(f"Error during smoothing in MNI space:\n{e}")
            return
        
        # Tissue segmentation in MNI
        print("\n")
        print("GM, WM, CSF segmentation in MNI152 space...")
        input_PET = os.path.join(self.var_output_path.get(), "pet_coreg_brain_MNI_smooth.nii.gz")
        # Need to check which MRI modality was used
        if os.path.exists(os.path.join(self.var_output_path.get(), "Mask_t1_GM_MNI.nii.gz")):
            # T1 modality
            mask_GM = os.path.join(self.var_output_path.get(), "Mask_t1_GM_MNI.nii.gz")
            mask_WM = os.path.join(self.var_output_path.get(), "Mask_t1_WM_MNI.nii.gz")
            mask_CSF = os.path.join(self.var_output_path.get(), "Mask_t1_CSF_MNI.nii.gz")
        elif os.path.exists(os.path.join(self.var_output_path.get(), "Mask_t2_GM_MNI.nii.gz")):
            # T2 modality
            mask_GM = os.path.join(self.var_output_path.get(), "Mask_t2_GM_MNI.nii.gz")
            mask_WM = os.path.join(self.var_output_path.get(), "Mask_t2_WM_MNI.nii.gz")
            mask_CSF = os.path.join(self.var_output_path.get(), "Mask_t2_CSF_MNI.nii.gz")
        else:    
            # Flair modality
            mask_GM = os.path.join(self.var_output_path.get(), "Mask_flair_GM_MNI.nii.gz")
            mask_WM = os.path.join(self.var_output_path.get(), "Mask_flair_WM_MNI.nii.gz")
            mask_CSF = os.path.join(self.var_output_path.get(), "Mask_flair_CSF_MNI.nii.gz")
        out_GM = os.path.join(self.var_output_path.get(), "pet_GM_MNI.nii.gz")
        out_WM = os.path.join(self.var_output_path.get(), "pet_WM_MNI.nii.gz")
        out_CSF = os.path.join(self.var_output_path.get(), "pet_CSF_MNI.nii.gz")

        try:
            ipf.apply_mask(input_PET, mask_GM, out_GM)
            ipf.apply_mask(input_PET, mask_WM, out_WM)
            ipf.apply_mask(input_PET, mask_CSF, out_CSF)
            print("Registration of Image segments to MNI152 space completed successfully.")
        except Exception as e:
            print(f"Error during registration of image segments to MNI152 space:\n{e}")
            return

        t2 = time.time()
        print("\nFinished processing.")
        print(f"Total time: {(t2-t1)/60:.2f} minutes")
    

    def btn_show_reg_result(self):
        try:
            MNI_path = os.path.join(os.getcwd(), "Templates/MNI152_T1_2mm_brain.nii.gz")
            reg_img_path = os.path.join(self.var_output_path.get(), "pet_coreg_brain_MNI.nii.gz")
            ipf.plot_overlay(MNI_path, reg_img_path, "Registration Result: MNI (background) and PET (overlay)")
        except Exception as e:
            print(f"Error displaying registration result:\n{e}")

    def btn_show_seg_result(self):
        try:
            gm_path = os.path.join(self.var_output_path.get(), "pet_GM_MNI.nii.gz")
            wm_path = os.path.join(self.var_output_path.get(), "pet_WM_MNI.nii.gz")
            csf_path = os.path.join(self.var_output_path.get(), "pet_CSF_MNI.nii.gz")
            ipf.plot_3_images_overlay(gm_path, wm_path, csf_path, 
                                    "Tissue Segmentation Result in MNI space")
        except Exception as e:
            print(f"Error displaying segmentation result:\n{e}")



# -------------------------------
# Log class
# -------------------------------
"""
It is aseparate class to print the output log inside the log box in GUI
"""
class StdoutRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", string)
        self.textbox.see("end")  # Auto-scroll
        self.textbox.configure(state="disabled")

    def flush(self):
        pass