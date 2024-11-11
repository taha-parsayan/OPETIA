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
import subprocess
import commands
import shutil
import fnmatch
import sys



root = Tk()
root.geometry("500x195+950+250")
root.resizable(False, False)
root.title("NIFTI organizer")


#___Variables
var_address_input = StringVar()
var_address_input.set('Not defined...')
var_check_open_files = StringVar()
var_check_open_files.set('0')

black_list = []

#___commands
def btn_enter_address_command():
    path = myfunctions.get_address_folder()
    var_address_input.set(path)

def btn_open_folder_command():
    webbrowser.open(var_address_input.get())
    
def btn_process_command():
    '''
    First move every nifti file to their corresponding sibject folder.
    Then rename them to T1 and PET.
    '''
    
    print('----------------Nifti organizer----------------')
    
    #Moving files
    print('  ')
    print('---Moving Nifti files to subject folders')
    main_directory = var_address_input.get()
    
    for subject_folder in os.listdir(main_directory):
        subject_path = os.path.join(main_directory, subject_folder)

        # Check if this is indeed a directory
        if not os.path.isdir(subject_path):
            continue

        # Loop through files in the main directory to find matches
        for file in os.listdir(main_directory):
            file_path = os.path.join(main_directory, file)

            # Skip directories and non-NIfTI files
            if os.path.isdir(file_path) or not file.endswith('.nii'):
                continue

            # Check if the file contains the subject ID (exact match within filename)
            if subject_folder in file:
                # Move the file to the subject folder
                new_file_path = os.path.join(subject_path, os.path.basename(file))
                shutil.move(file_path, new_file_path)
                         
            
    
    #Renaming files
    print('---Renaming the files to T1 and PET & unzipping PET')
    # Define the keywords for T1 and PET
    t1_keywords = ['t1', 'mri', 'mprage', 'mp-rage', 'mp_rage']
    pet_keywords = ['pet', 'fdg', 'f-18', 'static']
    
    # Function to check if any keyword is in the filename
    def contains_keyword(filename, keywords):
        return any(keyword in filename.lower() for keyword in keywords)
       
    # Check if any subject has more than a T1 and a PET
    for item in os.listdir(main_directory):
        item_path = os.path.join(main_directory, item)
        if os.path.isdir(item_path):
            nii_count = 0
            for file in os.listdir(item_path):
                file_path = os.path.join(item_path, file)
                if file.endswith('.nii') and os.path.isfile(file_path):
                    nii_count += 1
            if nii_count == 2:
                for file in os.listdir(item_path):
                    file_path = os.path.join(item_path, file)
                    if file.endswith('.nii') and os.path.isfile(file_path):
                        if contains_keyword(file, t1_keywords):
                            new_name = 'T1.nii'
                        elif contains_keyword(file, pet_keywords):
                            new_name = 'PET.nii' 
                        else:
                            continue

                        # Create the full path for renaming
                        old_path = file_path
                        new_path = os.path.join(item_path, new_name)

                        # Rename the file if the new name is different
                        if old_path != new_path:
                            os.rename(old_path, new_path)
                        
                        path_PET = os.path.join(item_path, 'PET.nii')
                        if os.path.exists(path_PET):
                            os.system('fslsplit ' + item_path + '/PET.nii ' + item_path + '/vol')
                            os.system('gunzip ' + item_path + '/vol*.nii.gz')
                            path_vol = os.path.join(item_path, 'vol0000.nii.gz')
                            if os.path.exists(path_vol):
                                os.system('rm ' + item_path + '/vol*.nii.gz')
                            
                    
                    
            elif nii_count != 2:
                black_list.append(item_path)
    
    
    print('Done')


           
    # Check files
    for folder_name in os.listdir(main_directory):
        address1 = os.path.join(main_directory, folder_name, 'T1.nii')
        address2 = os.path.join(main_directory, folder_name, 'PET.nii')
        if not os.path.exists(address1):
            print('  ')
            print('------ Could not create: '+ address1)
            if var_check_open_files.get() == '1':
                path_open = os.path.join(main_directory, folder_name)
                webbrowser.open(path_open)
            
        if not os.path.exists(address2):
            print('  ')
            print('------ Could not create: '+ address2)
            if var_check_open_files.get() == '1':
                path_open = os.path.join(main_directory, folder_name)
                webbrowser.open(path_open)
    
    print('Done')
    

                    
                    
# /work/TahaPourmaohammad#7093/KAN-project/AD/ADNI

#___GUI
frame1 = LabelFrame(root, text = 'Input parameters')
frame1.config(relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=115)

label1 = Label(frame1, text = "Folder including the NIFTI data and subject folders:").place(x=5,y=5)
btn_enter_address = Button(frame1, text = "Browse", command = btn_enter_address_command).place(x=5, y=30)
entr_address_structural_input = Entry(frame1, textvariable = var_address_input).place(x=100, y=35, width=365)

checkbutton_open_files = Checkbutton(frame1, variable = var_check_open_files, text='Open subject folders that need to be checked').place(x=5, y=70)

btn_process = Button(root, text="Start processing", command = btn_process_command).place(x=5, y=160)
btn_open_folder = Button(root, text="Open output folder", command = btn_open_folder_command).place(x=145,y=160)

root.mainloop()
