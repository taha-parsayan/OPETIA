import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import myfunctions
import webbrowser
import time
import threading
import subprocess
import platform
import fnmatch

root = tk.Tk()
root.geometry("500x705+0+0")
root.resizable(False, False)
root.title("PET image pre-processing")


# ___Variables
var_file_address_input = tk.StringVar()
var_file_address_input.set('Not defined...')
var_pet_address_output = tk.StringVar()
var_pet_address_output.set('Not defined...')
var_BET_threshold = tk.StringVar()
var_BET_threshold.set('0.5')
var_BET_g = tk.StringVar()
var_BET_g.set('0')
var_BET_function = tk.StringVar()
var_BET_function.set('Standard brain extraction using bet2')
var_reg_pet2highrez_dof = tk.StringVar()
var_reg_pet2highrez_dof.set('Rigid body - 6DOF')
var_reg_pet2highrez_ref = tk.StringVar()
var_reg_pet2highrez_ref.set('Not defined...')
var_reg_highrez2std_dof = tk.StringVar()
var_reg_highrez2std_dof.set('Translation only - 3DOF')
var_reg_matrix_ref_b2c = tk.StringVar()
var_reg_matrix_ref_b2c.set('Not defined...')
var_reg_cost = tk.StringVar()
var_reg_cost.set('Mutual information')
var_reg_interp = tk.StringVar()
var_reg_interp.set('Tri-linear')
var_smooth_check_btn = tk.StringVar()
var_smooth_check_btn.set(0)
var_smooth_fwhm = tk.StringVar()
var_smooth_fwhm.set('5')
var_thrp_check_btn = tk.StringVar()
var_thrp_check_btn.set(0)
var_thrp_percentage = tk.StringVar()
var_thrp_percentage.set('10')
var_reg_std_ref = tk.StringVar()
var_reg_std_ref.set("Templates/MNI152_T1_2mm_brain.nii.gz")



# ___Commands
def btn_enter_pet_input_command():
    path = myfunctions.get_address_folder()
    var_file_address_input.set(path)
    var_pet_address_output.set(var_file_address_input.get() + '/OPETIA_output')
    var_reg_matrix_ref_b2c.set(var_pet_address_output.get() + '/structural2std.mat')
    var_reg_pet2highrez_ref.set(var_pet_address_output.get() + '/structural_brain.nii.gz')

def btn_show_image_command():
    img1 = var_pet_address_output.get() + '/PET_brain_std.nii.gz'
    img2 = var_pet_address_output.get() + '/structural_brain_std.nii.gz'
    img3 = var_pet_address_output.get() + '/pet_quality_control.png'
    os.system('slicer ' + img1 + ' ' + img2 + ' -A 1500 ' + img3)
    
    if platform.system() == 'Linux':
        os.system(f'eog "{img3}" &')
    elif platform.system() == 'Darwin':
        os.system(f'open "{img3}"')


def btn_enter_pet_output_command():
    path = myfunctions.get_address_folder()
    var_pet_address_output.set(path)
    var_reg_matrix_ref_b2c.set(var_pet_address_output.get() + '/structural2std.mat')
    var_reg_pet2highrez_ref.set(var_pet_address_output.get() + '/structural_brain.nii.gz')

def btn_open_folder_command():
    if is_mac():
            subprocess.call(["open", var_file_address_input.get()])
    elif is_linux():
            subprocess.call(["xdg-open", var_file_address_input()])

def is_mac():
    return platform.system() == 'Darwin'

def is_linux():
    return platform.system() == 'Linux'

def find_PET_volumes(folder):
    return sorted(fnmatch.filter(os.listdir(folder), 'vol*.nii.gz'))

def btn_process_command():
    if var_file_address_input.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the PET image address")
    elif var_file_address_input.get() == "":
        messagebox.showinfo("Error...", "Please fill the PET image address")
    elif var_pet_address_output.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_pet_address_output.get() == "":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_reg_pet2highrez_ref.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the registration reference address")
    elif var_reg_pet2highrez_ref.get() == "":
        messagebox.showinfo("Error...", "Please fill the registration reference address")
    elif var_reg_matrix_ref_b2c.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the registration matrix address")
    elif var_reg_matrix_ref_b2c.get() == "":
        messagebox.showinfo("Error...", "Please fill the registration matrix address")
    elif var_reg_std_ref.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the registration matrix address")
    elif var_reg_std_ref.get() == "":
        messagebox.showinfo("Error...", "Please fill the registration matrix address")
    else:
        print('e\n')
        print('----------------PET image pre-processing----------------')
        print('--->Extracting the brain')

        pet_dir = var_file_address_input.get()
        pet_vols = find_PET_volumes(pet_dir)

        for vol_name in pet_vols:
            input_file = os.path.join(pet_dir, vol_name)
            output_file = os.path.join(var_pet_address_output.get(), vol_name.replace('.nii.gz', '_brain.nii.gz'))
            myfunctions.FSL_Brain_Extraction(input_file, output_file, var_BET_threshold.get(), var_BET_function.get(), var_BET_g.get())
        print('Done')

        print('--->Registering PET image to native structural space using FLIRT')

        reg_ref = var_reg_pet2highrez_ref.get()  # T1.nii.gz
        reg_model = var_reg_pet2highrez_dof.get()
        reg_cost = var_reg_cost.get()
        reg_interp = var_reg_interp.get()

        # Update PET volume list to skull-stripped versions
        pet_vols = [vol.replace('.nii.gz', '_brain.nii.gz') for vol in pet_vols]
        num_vols = len(pet_vols)
        print(f'Found {num_vols} PET volumes')

        if num_vols == 0:
            print('No PET volumes found!')
            return

        if num_vols == 1:
            # Single volume case: register directly to T1
            input_file = os.path.join(var_pet_address_output.get(), pet_vols[0])
            output_file = os.path.join(var_pet_address_output.get(), 'PET.nii.gz')
            matrix_file = os.path.join(var_pet_address_output.get(), 'pet2structural.mat')
            myfunctions.register_flirt(input_file, output_file, reg_ref, reg_model, matrix_file, reg_cost, reg_interp)
            print('Done')

        else:
            # Multiple volumes
            registered_vols = []

            # Step 1: Register vol0000 to T1
            input_file_0 = os.path.join(var_pet_address_output.get(), pet_vols[0])
            output_file_0 = os.path.join(var_pet_address_output.get(), 'PET_reg_0.nii.gz')
            matrix_file_0 = os.path.join(var_pet_address_output.get(), 'pet2structural.mat')
            myfunctions.register_flirt(input_file_0, output_file_0, reg_ref, reg_model, matrix_file_0, reg_cost, reg_interp)
            registered_vols.append(output_file_0)

            # Step 2: Register remaining volumes to PET_reg_0
            for i, vol_name in enumerate(pet_vols[1:], start=1):
                input_file = os.path.join(var_pet_address_output.get(), vol_name)
                output_file = os.path.join(var_pet_address_output.get(), f'PET_reg_{i}.nii.gz')
                matrix_file = os.path.join(var_pet_address_output.get(), f'pet2pet_reg_{i}.mat')
                myfunctions.register_flirt(input_file, output_file, output_file_0, '6', matrix_file, reg_cost, reg_interp)
                registered_vols.append(output_file)

            # Step 3: Sum all registered PET volumes
            output_pet = os.path.join(var_pet_address_output.get(), 'PET_brain.nii.gz')
            cmd = ['fslmaths', registered_vols[0]]
            for vol in registered_vols[1:]:
                cmd += ['-add', vol]
            cmd.append(output_pet)
            os.system(' '.join(cmd))
            print('Done')

        print('--->Warping PET image to MNI space using T1-to-MNI warp')

        # Paths
        reg_input = os.path.join(var_pet_address_output.get(), 'PET_brain.nii.gz')           # PET already in T1 space
        reg_output = os.path.join(var_pet_address_output.get(), 'PET_brain_std.nii.gz')      # Output in MNI space
        reg_ref = var_reg_std_ref.get()                                                      # MNI standard reference (e.g., MNI152_T1_2mm_brain.nii.gz)
        warp_file = os.path.join(var_pet_address_output.get(), 'structural_brain_std_warpcoef.nii.gz')  # FNIRT warp output from T1 to MNI

        # Apply warp
        os.system(
            f'applywarp --in={reg_input} --ref={reg_ref} --warp={warp_file} --out={reg_output}'
        )

        print('Done')

        if var_smooth_check_btn.get() == '1':
            print('--->Gaussian smoothing the registered PET image')
            smooth_sigma = float(var_smooth_fwhm.get()) / 2.3548
            os.system('fslmaths ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz -kernel gauss ' + str(smooth_sigma) + ' -fmean ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz' )
            print('Done')

        if var_thrp_check_btn.get() == '1':
            print('--->Thresholding the registered PET image')
            os.system('fslmaths ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz -thrp ' + var_thrp_percentage.get() + ' ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz' )
            print('Done')

        print('\n')
        print('Finish!')
        print('--------------------------------------------')


def btn_reg_structural_ref_command():
    path = myfunctions.get_address_file()
    var_reg_pet2highrez_ref.set(path)


def btn_reg_matrix_ref_command():
    path = myfunctions.get_address_file_reg_matrix((var_file_address_input.get()))
    var_reg_matrix_ref_b2c.set(path)


def btn_reg_std_ref_command():
    path = myfunctions.get_address_file_reg_reference()
    var_reg_std_ref.set(path)


# ___GUI
frame1 = tk.LabelFrame(root, text='Define input/output')
frame1.config(relief=tk.SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=150)

frame2 = tk.LabelFrame(root, text = 'Brain Extraction (set BET parameters)')
frame2.config(relief=tk.SUNKEN, bd=2)
frame2.place(x=5, y=170, width=490, height=80)

frame3 = tk.LabelFrame(root, text = 'Registration (native PET space to standard space)')
frame3.config(relief=tk.SUNKEN, bd=2)
frame3.place(x=5, y=265, width=490, height=230)

frame4 = tk.LabelFrame(root, text = 'Increase image signal to noise ratio')
frame4.config(relief=tk.SUNKEN, bd=2)
frame4.place(x=5, y=510, width=490, height=80)

label1 = tk.Label(frame1, text = "Folder containing the PET volumes:").place(x=5,y=5)
btn_enter_pet_input = tk.Button(frame1, text = "Browse", command = btn_enter_pet_input_command).place(x=5, y=30)
entr_address_structural_input = tk.Entry(frame1, textvariable = var_file_address_input).place(x=100, y=35, width=365)


label2 = tk.Label(frame1, text = "Output folder:").place(x=5, y=70)
btn_enter_pet_output = tk.Button(frame1, text="Browse", command = btn_enter_pet_output_command).place(x=5, y=95)
entr_address_pet_output = tk.Entry(frame1, textvariable = var_pet_address_output).place(x=100, y=100, width=365)

label3 = tk.Label(frame2, text = "Fractional intensity threshold:").place(x=5,y=5)
entr_BET_threshold = tk.Entry(frame2, textvariable = var_BET_threshold).place(x=190,y=5, width=35)

label4 = tk.Label(frame2, text = "Vertical gradient:").place(x=315,y=5)
entr_BET_g = tk.Entry(frame2, textvariable = var_BET_g).place(x=425,y=5, width=35)

label5 = tk.Label(frame2, text="Brain extraction function:").place(x=5, y=30)
combo_BET_function = ttk.Combobox(frame2, textvariable=var_BET_function, values=('Standard brain extraction using bet2', 'Robust brain centre estimation',
'Eye & optic nerve cleanup', 'Bias field & neck cleanup')).place(x=200, y=30, width=260)

label6 = tk.Label(frame3, text = "Brain extracted T1 in native space (structural_brain.nii.gz):").place(x=5, y=5)
btn_reg_structural_ref = tk.Button(frame3, text = "Browse", command = btn_reg_structural_ref_command).place(x=5, y=30)
entr_reg_structural_ref = tk.Entry(frame3, textvariable = var_reg_pet2highrez_ref).place(x=100, y=30, width=365)

label7 = tk.Label(frame3, text = "Standard template (MNI152_T1_2mm_brain.nii.gz):").place(x=5, y=65)
btn_reg_std_ref = tk.Button(frame3, text = "Browse", command = btn_reg_std_ref_command).place(x=5, y=90)
entr_reg_std_ref = tk.Entry(frame3, textvariable = var_reg_std_ref).place(x=100, y=90, width=365)

label8 = tk.Label(frame3, text = "PET to T1 registration model (DOF):").place(x=5, y=125)
combo_reg_pet2highrez_dof = ttk.Combobox(frame3, textvariable=var_reg_pet2highrez_dof, values=('Rigid body - 6DOF', 'Affine - 12DOF', 'Nonlinear - 9DOF')).place(x=267, y=125, width=200)

label9 = tk.Label(frame3, text = "PET to T1 Cost function:").place(x=5, y=150)
combo_reg_cost = ttk.Combobox(frame3, textvariable=var_reg_cost, values=('Mutual information', 'Least squares', 'Normalized mutual information')).place(x=267, y=150, width=200)

label10 = tk.Label(frame3, text = "PET to T1 interpolation method:").place(x=5, y=180)
combo_reg_interp = ttk.Combobox(frame3, textvariable=var_reg_interp, values=('Tri-linear', 'Nearest neighbor', 'Spline')).place(x=267, y=180, width=200)

label11 = tk.Label(frame4, text="Smooth the PET image").place(x=30,y=5)
check_smooth = tk.Checkbutton(frame4, variable=var_smooth_check_btn, onvalue='1', offvalue='0').place(x=5, y=5)
entr_smooth_fwhm = tk.Entry(frame4, textvariable=var_smooth_fwhm).place(x=225, y=5, width=60)

label12 = tk.Label(frame4, text="Threshold the PET image").place(x=30,y=30)
check_thrp = tk.Checkbutton(frame4, variable=var_thrp_check_btn, onvalue='1', offvalue='0').place(x=5, y=30)
entr_thrp_percentage = tk.Entry(frame4, textvariable=var_thrp_percentage).place(x=225, y=30, width=60)

btn_process = tk.Button(root, text="Process", command=btn_process_command).place(x=5, y=595, width=490)

btn_show_image = tk.Button(root, text="Show processed image", command=btn_show_image_command).place(x=5, y=630, width=490)

btn_open_folder = tk.Button(root, text="Open output folder", command=btn_open_folder_command).place(x=5, y=665, width=490)

root.mainloop()
