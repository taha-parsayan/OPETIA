from tkinter import *
import os
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
from tkinter import messagebox
import myfunctions
import webbrowser
import subprocess
import shutil
import fnmatch
import sys

root = Tk()
root.geometry("500x195+0+0")
root.resizable(False, False)
root.title("NIFTI organizer")

#___Variables
var_address_input = StringVar(value='Not defined...')
var_check_open_files = StringVar(value='0')

black_list = []

#___commands
def btn_enter_address_command():
    path = myfunctions.get_address_folder()
    var_address_input.set(path)

def btn_open_folder_command():
    webbrowser.open(var_address_input.get())
    
def btn_process_command():
    print('----------------Nifti organizer----------------')
    
    print('  ')
    print('---Moving Nifti files to subject folders')
    main_directory = var_address_input.get()
    
    for subject_folder in os.listdir(main_directory):
        subject_path = os.path.join(main_directory, subject_folder)
        if not os.path.isdir(subject_path):
            continue

        for file in os.listdir(main_directory):
            file_path = os.path.join(main_directory, file)
            if os.path.isdir(file_path) or not file.endswith('.nii'):
                continue

            if subject_folder in file:
                new_file_path = os.path.join(subject_path, os.path.basename(file))
                shutil.move(file_path, new_file_path)
                          
    print('---Renaming the files to T1 and PET & unzipping PET')
    t1_keywords = ['t1', 'mri', 'mprage', 'mp-rage', 'mp_rage']
    pet_keywords = ['pet', 'fdg', 'f-18', 'static']
    
    def contains_keyword(filename, keywords):
        return any(keyword in filename.lower() for keyword in keywords)
       
    for item in os.listdir(main_directory):
        item_path = os.path.join(main_directory, item)
        if os.path.isdir(item_path):
            nii_count = sum(1 for file in os.listdir(item_path) if file.endswith('.nii'))
            if nii_count == 2:
                for file in os.listdir(item_path):
                    file_path = os.path.join(item_path, file)
                    if file.endswith('.nii'):
                        if contains_keyword(file, t1_keywords):
                            new_name = 'T1.nii'
                        elif contains_keyword(file, pet_keywords):
                            new_name = 'PET.nii' 
                        else:
                            continue

                        new_path = os.path.join(item_path, new_name)
                        if file_path != new_path:
                            os.rename(file_path, new_path)
                        
                        path_PET = os.path.join(item_path, 'PET.nii')
                        if os.path.exists(path_PET):
                            subprocess.run(['fslsplit', path_PET, os.path.join(item_path, 'vol')])
                            subprocess.run(['gunzip'] + list(fnmatch.filter(os.listdir(item_path), 'vol*.nii.gz')))
                            path_vol = os.path.join(item_path, 'vol0000.nii.gz')
                            if os.path.exists(path_vol):
                                subprocess.run(['rm'] + list(fnmatch.filter(os.listdir(item_path), 'vol*.nii.gz')))
                    
            elif nii_count != 2:
                black_list.append(item_path)
    
    print('Done')

    for folder_name in os.listdir(main_directory):
        address1 = os.path.join(main_directory, folder_name, 'T1.nii')
        address2 = os.path.join(main_directory, folder_name, 'PET.nii')
        if not os.path.exists(address1):
            print('  ')
            print('------ Could not create: '+ address1)
            if var_check_open_files.get() == '1':
                webbrowser.open(os.path.join(main_directory, folder_name))
        
        if not os.path.exists(address2):
            print('  ')
            print('------ Could not create: '+ address2)
            if var_check_open_files.get() == '1':
                webbrowser.open(os.path.join(main_directory, folder_name))
    
    print('Done')

#___GUI
frame1 = LabelFrame(root, text='Input parameters', relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=115)

Label(frame1, text="Folder including the NIFTI data and subject folders:").place(x=5, y=5)
Button(frame1, text="Browse", command=btn_enter_address_command).place(x=5, y=30)
Entry(frame1, textvariable=var_address_input).place(x=100, y=35, width=365)

Checkbutton(frame1, variable=var_check_open_files, text='Open subject folders that need to be checked').place(x=5, y=70)

Button(root, text="Start processing", command=btn_process_command).place(x=5, y=160)
Button(root, text="Open output folder", command=btn_open_folder_command).place(x=145, y=160)

root.mainloop()
