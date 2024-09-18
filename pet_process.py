from Tkinter import *
import os
import ttk
import tkFileDialog
from tkFileDialog import askopenfile
import tkMessageBox as messagebox
import myfunctions
import webbrowser
import time
import threading

root = Tk()
root.geometry("500x760+950+250")
root.resizable(False, False)
root.title("PET image pre-processing")


#___Variables
var_pet_address_input = StringVar()
var_pet_address_input.set('Not defined...')
var_pet_address_output = StringVar()
var_pet_address_output.set('Not defined...')
var_BET_threshold = StringVar()
var_BET_threshold.set('0.5')
var_BET_function = StringVar()
var_BET_function.set('Standard brain extraction using bet2')
var_reg_pet2highrez_dof = StringVar()
var_reg_pet2highrez_dof.set('Rigid body - 6DOF')
var_reg_pet2highrez_ref = StringVar()
var_reg_pet2highrez_ref.set('Not defined...')
var_reg_highrez2std_dof = StringVar()
var_reg_highrez2std_dof.set('Translation only - 3DOF')
var_reg_matrix_ref_b2c = StringVar()
var_reg_matrix_ref_b2c.set('Not defined...')
var_reg_std_ref = StringVar()
var_reg_std_ref.set('/opt/easybuild/software/FSL/6.0.3-foss-2019b-Python-3.7.4/fsl/data/standard/MNI152lin_T1_2mm_brain.nii.gz')
var_reg_cost = StringVar()
var_reg_cost.set('Mutual information')
var_reg_interp = StringVar()
var_reg_interp.set('Tri-linear')
var_smooth_check_btn = StringVar()
var_smooth_check_btn.set(0)
var_smooth_fwhm = StringVar()
var_smooth_fwhm.set('5')
var_thrp_check_btn = StringVar()
var_thrp_check_btn.set(0)
var_thrp_percentage = StringVar()
var_thrp_percentage.set('10')


#___Commands
def btn_enter_pet_input_command():
    path = myfunctions.get_address_file()
    var_pet_address_input.set(path)
    (dirname, filename) = os.path.split(var_pet_address_input.get())
    os.system('mkdir ' + dirname + '/OPETIA_output')
    var_pet_address_output.set(dirname + '/OPETIA_output')
    var_reg_matrix_ref_b2c.set(var_pet_address_output.get() + '/structural2std.mat')
    var_reg_pet2highrez_ref.set(var_pet_address_output.get() + '/structural_brain.nii.gz')

def btn_show_image_command():
    #os.system("fsleyes " + var_pet_address_input.get())
    img1 = var_pet_address_output.get() + '/PET_brain_std.nii.gz'
    img2 = var_pet_address_output.get() + '/structural_brain_std.nii.gz'
    img3 = var_pet_address_output.get() + '/pet_quality_control.png'
    os.system('slicer ' + img1 + ' ' + img2 + ' -A 1500 ' + img3)
    os.system('eog ' + img3)


def btn_enter_pet_output_command():
    path = myfunctions.get_address_folder()
    var_pet_address_output.set(path)
    var_reg_matrix_ref_b2c.set(var_pet_address_output.get() + '/structural2std.mat')
    var_reg_pet2highrez_ref.set(var_pet_address_output.get() + '/structural_brain.nii.gz')

def btn_open_folder_command():
    webbrowser.open(var_pet_address_output.get())

def btn_process_command():
    if var_pet_address_input.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the PET image address")
    elif var_pet_address_input.get() == "":
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
        os.system('echo ')
        os.system('echo ----------------PET image pre-processing----------------')
        os.system('echo ')
        os.system('echo ---Extracting the brain')
        myfunctions.FSL_Brain_Extraction(var_pet_address_input.get(), var_pet_address_output.get() + '/PET_brain.nii.gz', var_BET_threshold.get(), var_BET_function.get())
        os.system('echo Done')

        os.system('echo ---Registering PET image to native structural space using FLIRT')
        reg_input = var_pet_address_output.get() + '/PET_brain.nii.gz'
        reg_output = var_pet_address_output.get() + '/PET_brain_native_structural.nii.gz'
        reg_ref = var_reg_pet2highrez_ref.get()
        reg_model = var_reg_pet2highrez_dof.get()
        matrix_name = var_pet_address_output.get() + '/pet2structural.mat'
        reg_cost = var_reg_cost.get()
        reg_interp = var_reg_interp.get()
        myfunctions.register_flirt(reg_input, reg_output, reg_ref, reg_model, matrix_name, reg_cost, reg_interp)
        os.system('echo Done')

        os.system('echo ---Registering PET image to standard space using transformation matrix')
        reg_input = var_pet_address_output.get() + '/PET_brain.nii.gz'
        reg_output = var_pet_address_output.get() + '/PET_brain_std.nii.gz'
        reg_mat_a2b = var_pet_address_output.get() + '/pet2structural.mat'
        reg_mat_b2c = var_reg_matrix_ref_b2c.get()
        reg_ref = var_reg_std_ref.get()

        os.system('convert_xfm -omat ' + var_pet_address_output.get() + '/pet2std.mat ' + '-concat ' + reg_mat_b2c + ' ' + reg_mat_a2b)

        reg_mat_a2c = var_pet_address_output.get() + '/pet2std.mat'
        myfunctions.register_using_matrix(reg_input, reg_output, reg_mat_a2c, reg_ref)

        os.system('echo Done')

        if var_smooth_check_btn.get() == '1':
            os.system('echo ---Gaussian smoothing the registered PET image')
            smooth_sigma = float(var_smooth_fwhm.get()) / 2.3548
            os.system('fslmaths ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz -kernel gauss ' + str(smooth_sigma) + ' -fmean ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz' )
            os.system('echo Done')

        if var_thrp_check_btn.get() == '1':
            os.system('echo ---Thresholding the registered PET image')
            os.system('fslmaths ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz -thrp ' + var_thrp_percentage.get() + ' ' + var_pet_address_output.get() + '/PET_brain_std.nii.gz' )
            os.system('echo Done')



        os.system('echo ')
        os.system('echo ----------Finish!')
        os.system('echo --------------------------------------------')
        os.system('echo ')


def btn_reg_structural_ref_command():
    path = myfunctions.get_address_file()
    var_reg_pet2highrez_ref.set(path)


def btn_reg_matrix_ref_command():
    path = myfunctions.get_address_file_reg_matrix((var_pet_address_input.get()))
    var_reg_matrix_ref_b2c.set(path)


def btn_reg_std_ref_command():
    path = myfunctions.get_address_file_reg_reference()
    var_reg_std_ref.set(path)


#___GUI
frame1 = LabelFrame(root, text='Define input/output')
frame1.config(relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=150)

frame2 = LabelFrame(root, text = 'Brain Extraction (set BET parameters)')
frame2.config(relief=SUNKEN, bd=2)
frame2.place(x=5, y=170, width=490, height=110)

frame3 = LabelFrame(root, text = 'Registration (native PET space to standard space)')
frame3.config(relief=SUNKEN, bd=2)
frame3.place(x=5, y=295, width=490, height=300)

frame4 = LabelFrame(root, text = 'Increase image signal to noise ratio')
frame4.config(relief=SUNKEN, bd=2)
frame4.place(x=5, y=610, width=490, height=75)

label1 = Label(frame1, text = "Input PET image:").place(x=5,y=5)
btn_enter_pet_input = Button(frame1, text = "Browse", command = btn_enter_pet_input_command).place(x=5, y=30)
entr_address_structural_input = Entry(frame1, textvariable = var_pet_address_input).place(x=100, y=35, width=365)


label2 = Label(frame1, text = "Output folder:").place(x=5, y=70)
btn_enter_pet_output = Button(frame1, text="Browse", command = btn_enter_pet_output_command).place(x=5, y=95)
entr_address_pet_output = Entry(frame1, textvariable = var_pet_address_output).place(x=100, y=100, width=365)

label3 = Label(frame2, text = "Factional intensity threshold:").place(x=5,y=5)
entr_BET_threshold = Entry(frame2, textvariable = var_BET_threshold).place(x=425,y=5, width=35)

label4 = Label(frame2, text="Brain extraction function:").place(x=5, y=30)
combo_BET_function = ttk.Combobox(frame2, textvariable=var_BET_function, values=('Standard brain extraction using bet2', 'Robust brain centre estimation',
'Eye & optic nerve cleanup', 'Bias field & neck cleanup', 'Improve BET if FOV is very small in Z', 'Apply to 4D FMRI data',
'Run bet2 and then betsurf to get additional skull and scalp surfaces', 'As above, when also feeding in non-brain-extracted T2'), state= 'readonly').place(x=5, y=60, width=460)


label5 = Label(frame3, text='Degree of freedom (PET to structural):').place(x=5, y=5)
combo_reg_pet2highrez_dof = ttk.Combobox(frame3, textvariable=var_reg_pet2highrez_dof, values = ('Translation only - 3DOF', 'Rigid body - 6DOF', 'Gloval rescale - 7DOF',
'Traditional - 9DOF', 'Affine - 12DOF'), state= 'readonly').place(x=265, y=5, width=200)
label9 = Label(frame3, text="Cost function:").place(x=5,y=30)
combo_reg_cost = ttk.Combobox(frame3, textvariable=var_reg_cost, values = ('Correlation ratio', 'Mutual information', 'Normalised mutual information',
'Normalised correlation', 'Least squares'), state= 'readonly').place(x=265, y=30, width=200)
label10 = Label(frame3, text="Interpolation:").place(x=5,y=55)
combo_reg_interp = ttk.Combobox(frame3, textvariable=var_reg_interp, values = ('Tri-linear', 'Nearest neighbour', 'Spline',
'Sinc'), state= 'readonly').place(x=265, y=55, width=200)

label6 = Label(frame3, text='Native structural image (brain extracted):').place(x=5, y=90)
btn_reg_structural_ref = Button(frame3, text='Browse', command = btn_reg_structural_ref_command).place(x=5,y=115)
entr_reg_structural_ref = Entry(frame3, textvariable = var_reg_pet2highrez_ref).place(x=100, y=120, width=365)

label7 = Label(frame3, text='Registration reference (standard space):').place(x=5, y=155)
btn_reg_std_ref = Button(frame3, text='Browse', command = btn_reg_std_ref_command).place(x=5,y=180)
entr_reg_std_ref = Entry(frame3, textvariable = var_reg_std_ref).place(x=100, y=185, width=365)

label8 = Label(frame3, text='Structural to standard registration matrix:').place(x=5, y=220)
btn_reg_matrix_ref = Button(frame3, text='Browse', command = btn_reg_matrix_ref_command).place(x=5,y=245)
entr_reg_matrix_ref = Entry(frame3, textvariable = var_reg_matrix_ref_b2c).place(x=100, y=250, width=365)

checkbutton_smooth = Checkbutton(frame4, variable = var_smooth_check_btn, text='Gaussian smoothing with FWHM(mm) of:').place(x=5, y=5)
entr_smooth_fwhm = Entry(frame4, textvariable = var_smooth_fwhm).place(x=425, y=5, width=35)
checkbutton_thrp = Checkbutton(frame4, variable = var_thrp_check_btn, text='Threshold with (%):').place(x=5, y=30)
entr_thrp_percentage = Entry(frame4, textvariable = var_thrp_percentage).place(x=425, y=30, width=35)


btn_process = Button(root, text="Start processing", command = btn_process_command).place(x=5, y=725)
btn_show_image = Button(root, text="Show image", command=btn_show_image_command).place(x=145,y=725)
btn_open_folder = Button(root, text="Open output folder", command = btn_open_folder_command).place(x=260,y=725)




root.mainloop()
