from tkinter import *
import os
import tkinter.ttk as ttk
import tkinter.filedialog as tkFileDialog
from tkinter.filedialog import askopenfile
import tkinter.messagebox as messagebox
import myfunctions
import webbrowser
import time
import threading


root = Tk()
root.geometry("500x580+0+0")
root.resizable(False, False)
root.title("Structural image pre-processing")

#___Variables
var_structural_address_input = StringVar()
var_structural_address_input.set("Not defined...")
var_structural_address_output = StringVar()
var_structural_address_output.set("Not defined...")
var_BET_threshold = StringVar()
var_BET_threshold.set("0.5")
var_BET_function = StringVar()
var_BET_function.set('Standard brain extraction using bet2')
var_reg_dof = StringVar()
var_reg_dof.set('Affine - 12DOF')
var_reg_ref = StringVar()
var_reg_ref.set('/opt/easybuild/software/FSL/6.0.3-foss-2019b-Python-3.7.4/fsl/data/standard/MNI152lin_T1_2mm_brain.nii.gz')
var_reg_cost = StringVar()
var_reg_cost.set('Correlation ratio')
var_reg_interp = StringVar()
var_reg_interp.set('Tri-linear')
var_FAST_chechbtn = IntVar()
var_FAST_chechbtn.set(1)


#___Commands
def btn_enter_structural_input_command():
    path = myfunctions.get_address_file()
    var_structural_address_input.set(path)
    (dirname, filename) = os.path.split(var_structural_address_input.get())
    os.makedirs(dirname + '/OPETIA_output', exist_ok=True)
    var_structural_address_output.set(dirname + '/OPETIA_output')

def btn_show_image_command():
    img1 = var_structural_address_output.get() + '/structural_brain_std.nii.gz'
    img2 = '/opt/easybuild/software/FSL/6.0.3-foss-2019b-Python-3.7.4/fsl/data/standard/MNI152lin_T1_2mm_brain.nii.gz'
    img3 = var_structural_address_output.get() + '/structural_quality_control.png'
    os.system('slicer ' + img1 + ' ' + img2 + ' -A 1500 ' + img3)
    os.system('eog ' + img3)

def btn_enter_structural_output_command():
    path = myfunctions.get_address_folder()
    var_structural_address_output.set(path)

def btn_process_command():
    if var_structural_address_input.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the structural image address")
    elif var_structural_address_input.get() == "":
        messagebox.showinfo("Error...", "Please fill the structural image address")
    elif var_structural_address_output.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_structural_address_output.get() == "":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_reg_ref.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the registration reference")
    elif var_reg_ref.get() == "":
        messagebox.showinfo("Error...", "Please fill the registration reference")
    else:
        os.system('echo ')
        os.system('echo ----------------Structural image pre-processing----------------')
        os.system('echo ')
        os.system('echo ---Extracting the brain')
        myfunctions.FSL_Brain_Extraction(var_structural_address_input.get(), var_structural_address_output.get() + '/structural_brain.nii.gz', var_BET_threshold.get(), var_BET_function.get())
        os.system('echo Done')

        os.system('echo ---Registering structural image to standard space using FLIRT')
        reg_input = var_structural_address_output.get() + '/structural_brain.nii.gz'
        reg_output = var_structural_address_output.get() + '/structural_brain_std.nii.gz'
        reg_ref = var_reg_ref.get()
        reg_model = var_reg_dof.get()
        reg_cost = var_reg_cost.get()
        reg_interp = var_reg_interp.get()
        matrix_name = var_structural_address_output.get() + '/structural2std.mat'
        myfunctions.register_flirt(reg_input, reg_output, reg_ref, reg_model, matrix_name, reg_cost, reg_interp)
        os.system('echo Done')

        #if var_FAST_chechbtn.get() == 1:
        os.system('echo ---Native image tissue segmentation - GM,WM,CSF')
        fast_input = var_structural_address_output.get() + '/structural_brain.nii.gz'
        fast_output = var_structural_address_output.get()
        myfunctions.FSL_FAST(fast_input, fast_output)

        os.system('echo Done')

        os.system('echo ---Registering segments to standard space using FLIRT')
        reg_input = var_structural_address_output.get() + '/fast_pve_0.nii.gz'
        reg_output = var_structural_address_output.get() + '/fast_pve_0_std.nii.gz'
        reg_mat_b2c = var_structural_address_output.get() + '/structural2std.mat'
        reg_ref = var_reg_ref.get()
        myfunctions.register_using_matrix(reg_input, reg_output, reg_mat_b2c, reg_ref)

        reg_input = var_structural_address_output.get() + '/fast_pve_1.nii.gz'
        reg_output = var_structural_address_output.get() + '/fast_pve_1_std.nii.gz'
        reg_mat_b2c = var_structural_address_output.get() + '/structural2std.mat'
        reg_ref = var_reg_ref.get()
        myfunctions.register_using_matrix(reg_input, reg_output, reg_mat_b2c, reg_ref)

        reg_input = var_structural_address_output.get() + '/fast_pve_2.nii.gz'
        reg_output = var_structural_address_output.get() + '/fast_pve_2_std.nii.gz'
        reg_mat_b2c = var_structural_address_output.get() + '/structural2std.mat'
        reg_ref = var_reg_ref.get()
        myfunctions.register_using_matrix(reg_input, reg_output, reg_mat_b2c, reg_ref)


        os.system('fslmaths ' + fast_output + '/fast_pve_0_std.nii.gz ' + '-thr 0.3 ' + fast_output + '/csf_mask_std.nii.gz')
        os.system('fslmaths ' + fast_output + '/csf_mask_std.nii.gz ' + '-bin ' + fast_output + '/csf_mask_std.nii.gz')
        #os.system('fslmaths ' + fast_output + '/structural_brain_std.nii.gz ' + '-mul ' + fast_output + '/csf_mask_std.nii.gz ' + fast_output + '/csf_std.nii.gz')

        os.system('fslmaths ' + fast_output + '/fast_pve_1_std.nii.gz ' + '-thr 0.3 ' + fast_output + '/graymatter_mask_std.nii.gz')
        os.system('fslmaths ' + fast_output + '/graymatter_mask_std.nii.gz ' + '-bin ' + fast_output + '/graymatter_mask_std.nii.gz')
        #os.system('fslmaths ' + fast_output + '/structural_brain_std.nii.gz ' + '-mul ' + fast_output + '/graymatter_mask_std.nii.gz ' + fast_output + '/graymatter_std.nii.gz')

        os.system('fslmaths ' + fast_output + '/fast_pve_2_std.nii.gz ' + '-thr 0.3 ' + fast_output + '/whitematter_mask_std.nii.gz')
        os.system('fslmaths ' + fast_output + '/whitematter_mask_std.nii.gz ' + '-bin ' + fast_output + '/whitematter_mask_std.nii.gz')
        #os.system('fslmaths ' + fast_output + '/structural_brain_std.nii.gz ' + '-mul ' + fast_output + '/whitematter_mask_std.nii.gz ' + fast_output + '/whitematter_std.nii.gz')



        os.system('echo Done')

        os.system('echo ---')

        os.system('echo ')
        os.system('echo ----------Finish!')
        os.system('echo --------------------------------------------')
        os.system('echo ')

def btn_open_folder_command():
    webbrowser.open(var_structural_address_output.get())

def btn_reg_ref_command():
    path = myfunctions.get_address_file_reg_reference()
    var_reg_ref.set(path)

#___GUI
frame1 = LabelFrame(root, text='Define input/output')
frame1.config(relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=150)

frame2 = LabelFrame(root, text = 'Brain Extraction (set BET parameters)')
frame2.config(relief=SUNKEN, bd=2)
frame2.place(x=5, y=170, width=490, height=110)

frame3 = LabelFrame(root, text = 'Registration (native structural space to standard space)')
frame3.config(relief=SUNKEN, bd=2)
frame3.place(x=5, y=295, width=490, height=170)

# frame4 = LabelFrame(root, text = 'Tissue segmentation')
# frame4.config(relief=SUNKEN, bd=2)
# frame4.place(x=5, y=480, width=490, height=50)

label1 = Label(frame1, text = "Input structural image:").place(x=5,y=5)
btn_enter_structural_input = Button(frame1, text = "Browse", command = btn_enter_structural_input_command).place(x=5, y=30)
entr_address_structural_input = Entry(frame1, textvariable = var_structural_address_input).place(x=100, y=35, width=365)

label2 = Label(frame1, text = "Output folder:").place(x=5, y=70)
btn_enter_structural_output = Button(frame1, text="Browse", command = btn_enter_structural_output_command).place(x=5, y=95)
entr_address_structural_output = Entry(frame1, textvariable = var_structural_address_output).place(x=100, y=100, width=365)

label3 = Label(frame2, text = "Fractional intensity threshold:").place(x=5,y=5)
entr_BET_threshold = Entry(frame2, textvariable = var_BET_threshold).place(x=425,y=5, width=35)

label4 = Label(frame2, text="Function/Modality:").place(x=5, y=30)
combo_BET_function = ttk.Combobox(frame2, textvariable=var_BET_function, values=('Standard brain extraction using bet2', 'Robust brain centre estimation',
'Eye & optic nerve cleanup', 'Bias field & neck cleanup', 'Improve BET if FOV is very small in Z', 'Apply to 4D FMRI data',
'Run bet2 and then betsurf to get additional skull and scalp surfaces', 'As above, when also feeding in non-brain-extracted T2'), state= 'readonly').place(x=5, y=60, width=460)


label6 = Label(frame3, text='Reference:').place(x=5, y=5)
btn_reg_ref = Button(frame3, text='Browse', command = btn_reg_ref_command).place(x=5,y=30)
entr_reg_ref = Entry(frame3, textvariable = var_reg_ref).place(x=100, y=35, width=365)
label5 = Label(frame3, text='Degree of freedom:').place(x=5, y=75)
combo_reg_dof = ttk.Combobox(frame3, textvariable=var_reg_dof, values = ('Translation only - 3DOF', 'Rigid body - 6DOF', 'Gloval rescale - 7DOF',
'Traditional - 9DOF', 'Affine - 12DOF'), state= 'readonly').place(x=265, y=75, width=200)
label9 = Label(frame3, text="Cost function:").place(x=5,y=100)
combo_reg_cost = ttk.Combobox(frame3, textvariable=var_reg_cost, values = ('Correlation ratio', 'Mutual information', 'Normalised mutual information',
'Normalised correlation', 'Least squares'), state= 'readonly').place(x=265, y=100, width=200)

label10 = Label(frame3, text="Interpolation:").place(x=5, y=125)
combo_reg_interp = ttk.Combobox(frame3, textvariable=var_reg_interp, values = ('Nearest neighbour', 'Tri-linear', 'Spline', 'Lanczos'), state = 'readonly').place(x=265, y=125, width=200)

# label11 = Checkbutton(frame4, text = "Run FAST segmentation", variable = var_FAST_chechbtn).place(x=5, y=5)

btn_process = Button(root, text = "Process", command = btn_process_command).place(x=5, y=475, width=490)
                     
btn_show_image = Button(root, text = "Show processed image", command = btn_show_image_command).place(x=5, y=510, width=490)

btn_open_folder = Button(root, text="Open output folder", command = btn_open_folder_command).place(x=5, y=545, width=490)


root.mainloop()
