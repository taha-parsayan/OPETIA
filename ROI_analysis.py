from tkinter import *
import os
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
from tkinter import messagebox
import myfunctions
import webbrowser
import time
import threading
import subprocess
import shutil
import platform

root = Tk()
root.geometry("500x395+0+0")
root.resizable(False, False)
root.title("ROI analysis")


#___Variables
var_pet_address_input = StringVar(value='Not defined...')
var_pet_address_output = StringVar(value='Not defined...')
var_injected_dose = StringVar(value='1')
var_body_weight = StringVar(value='80')
var_type_of_measurement = StringVar(value='Using body weight')
var_type_of_SUV = StringVar(value='SUV mean')
var_height = StringVar(value='1.8')
var_SUV_reference = StringVar(value='Cerebellum')
var_atlas = StringVar(value='Harvard Oxford atlas')

#___commands
def btn_enter_pet_input_command():
    path = myfunctions.get_address_folder()
    var_pet_address_input.set(path)
    var_pet_address_output.set(var_pet_address_input.get() + '/ROI_analysis')

def btn_enter_pet_output_command():
    path = myfunctions.get_address_folder()
    var_pet_address_output.set(path)

def btn_open_folder_command():
    if is_mac():
            subprocess.call(["open", var_address_input.get()])
    elif is_linux():
            subprocess.call(["xdg-open", var_address_input()])

def is_mac():
    return platform.system() == 'Darwin'

def is_linux():
    return platform.system() == 'Linux'


def btn_process_command():
    if var_pet_address_input.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the PET image address")
    elif var_pet_address_input.get() == "":
        messagebox.showinfo("Error...", "Please fill the PET image address")
    elif var_pet_address_output.get() == "Not defined...":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_pet_address_output.get() == "":
        messagebox.showinfo("Error...", "Please fill the Output address")
    elif var_injected_dose.get() == "":
        messagebox.showinfo("Error...", "Please fill the injected dose")
    elif var_body_weight.get() == "":
        messagebox.showinfo("Error...", "Please fill the body weight")
    else:

        if var_atlas.get() == 'Harvard Oxford atlas':
            dirname = var_pet_address_input.get()
            os.system('mkdir ' + dirname + '/ROI_analysis')
            shutil.rmtree(var_pet_address_output.get())  #remove the folder to delete previous files
            os.system('mkdir ' + dirname + '/ROI_analysis')
            os.system('mkdir ' + dirname + '/ROI_analysis/Cortical_images')
            os.system('mkdir ' + dirname + '/ROI_analysis/Subcortical_images')
            os.system('mkdir ' + dirname + '/ROI_analysis/Cortical_normalized_images')
            os.system('mkdir ' + dirname + '/ROI_analysis/Subcortical_normalized_images')

            file_SUV_cortical_mean = open(var_pet_address_output.get() + '/SUV_cortical_mean.txt', 'w')
            file_SUV_cortical_mean.close()
            file_SUV_subcortical_mean = open(var_pet_address_output.get() + '/SUV_subcortical_mean.txt', 'w')
            file_SUV_subcortical_mean.close()
            file_SUVR_cortical_mean = open(var_pet_address_output.get() + '/SUVR_cortical_mean.txt', 'w')
            file_SUVR_cortical_mean.close()
            file_SUVR_subcortical_mean = open(var_pet_address_output.get() + '/SUVR_subcortical_mean.txt', 'w')
            file_SUVR_subcortical_mean.close()

            file_SUV_cortical_max = open(var_pet_address_output.get() + '/SUV_cortical_max.txt', 'w')
            file_SUV_cortical_max.close()
            file_SUV_subcortical_max = open(var_pet_address_output.get() + '/SUV_subcortical_max.txt', 'w')
            file_SUV_subcortical_max.close()
            file_SUVR_cortical_max = open(var_pet_address_output.get() + '/SUVR_cortical_max.txt', 'w')
            file_SUVR_cortical_max.close()
            file_SUVR_subcortical_max = open(var_pet_address_output.get() + '/SUVR_subcortical_max.txt', 'w')
            file_SUVR_subcortical_max.close()

            file_SUV_cortical_min = open(var_pet_address_output.get() + '/SUV_cortical_min.txt', 'w')
            file_SUV_cortical_min.close()
            file_SUV_subcortical_min = open(var_pet_address_output.get() + '/SUV_subcortical_min.txt', 'w')
            file_SUV_subcortical_min.close()
            file_SUVR_cortical_min = open(var_pet_address_output.get() + '/SUVR_cortical_min.txt', 'w')
            file_SUVR_cortical_min.close()
            file_SUVR_subcortical_min = open(var_pet_address_output.get() + '/SUVR_subcortical_min.txt', 'w')
            file_SUVR_subcortical_min.close()

            file_SUV_cortical_sd = open(var_pet_address_output.get() + '/SUV_cortical_sd.txt', 'w')
            file_SUV_cortical_sd.close()
            file_SUV_subcortical_sd = open(var_pet_address_output.get() + '/SUV_subcortical_sd.txt', 'w')
            file_SUV_subcortical_sd.close()
            file_SUVR_cortical_sd = open(var_pet_address_output.get() + '/SUVR_cortical_sd.txt', 'w')
            file_SUVR_cortical_sd.close()
            file_SUVR_subcortical_sd = open(var_pet_address_output.get() + '/SUVR_subcortical_sd.txt', 'w')
            file_SUVR_subcortical_sd.close()

            file_volume_cortical = open(var_pet_address_output.get() + '/Cortical_volume.txt', 'w')
            file_volume_cortical.close()
            file_volume_subcortical = open(var_pet_address_output.get() + '/Subcortical_volume.txt', 'w')
            file_volume_subcortical.close()

            os.system('cp Areas_Cortical.txt ' + var_pet_address_output.get())
            os.system('cp Areas_Subcortical.txt ' + var_pet_address_output.get())
            os.system('cp headers_cortical.txt ' + var_pet_address_output.get())
            os.system('cp headers_subcortical.txt ' + var_pet_address_output.get())

        elif var_atlas.get() == 'CortexID Suite atlas':
            dirname = var_pet_address_input.get()
            os.system('mkdir ' + dirname + '/ROI_analysis')
            shutil.rmtree(var_pet_address_output.get())  #remove the folder to delete previous files
            os.system('mkdir ' + dirname + '/ROI_analysis')
            os.system('mkdir ' + dirname + '/ROI_analysis/images')
            os.system('mkdir ' + dirname + '/ROI_analysis/normalized_images')

            file_SUV_cortical_mean = open(var_pet_address_output.get() + '/SUV_mean.txt', 'w')
            file_SUV_cortical_mean.close()
            file_SUVR_cortical_mean = open(var_pet_address_output.get() + '/SUVR_mean.txt', 'w')
            file_SUVR_cortical_mean.close()

            file_SUV_cortical_max = open(var_pet_address_output.get() + '/SUV_max.txt', 'w')
            file_SUV_cortical_max.close()
            file_SUVR_cortical_max = open(var_pet_address_output.get() + '/SUVR_max.txt', 'w')
            file_SUVR_cortical_max.close()

            file_SUV_cortical_min = open(var_pet_address_output.get() + '/SUV_min.txt', 'w')
            file_SUV_cortical_min.close()
            file_SUVR_cortical_min = open(var_pet_address_output.get() + '/SUVR_min.txt', 'w')
            file_SUVR_cortical_min.close()

            file_SUV_cortical_sd = open(var_pet_address_output.get() + '/SUV_sd.txt', 'w')
            file_SUV_cortical_sd.close()
            file_SUVR_cortical_sd = open(var_pet_address_output.get() + '/SUVR_sd.txt', 'w')
            file_SUVR_cortical_sd.close()

            file_volume_cortical = open(var_pet_address_output.get() + '/Volume.txt', 'w')
            file_volume_cortical.close()

            os.system('cp CortexID_areas.txt ' + var_pet_address_output.get())
            os.system('cp CortexID_headers.txt ' + var_pet_address_output.get())


        if var_SUV_reference.get() == 'Cerebellum':
            os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std' + ' -mul atlas_cortical/Cerebellum.nii.gz ' + \
            var_pet_address_input.get() + '/temp_img.nii.gz')
            #os.system('fslmaths ' + var_pet_address_output.get() + '/temp_img.nii.gz -bin ' + var_pet_address_output.get() + \
            # '/temp_img.nii.gz')
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_input.get() + \
             '/temp_img.nii.gz ' + var_pet_address_input.get() + '/PET_Cerebellum.nii.gz ')

            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebellum.nii.gz -M')
            L = len(x1)
            var_RA_refrence_mean = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebellum.nii.gz -P 0')
            L = len(x1)
            var_RA_refrence_min = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebellum.nii.gz -P 100')
            L = len(x1)
            var_RA_refrence_max = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebellum.nii.gz -S')
            L = len(x1)
            var_RA_reference_sd = x1[0:L-1]

        elif var_SUV_reference.get() == 'Cerebral cortex':
            os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std' + ' -mul atlas_subcortical/cerebral_cortex_bin.nii.gz ' + \
            var_pet_address_input.get() + '/temp_img.nii.gz')
            # os.system('fslmaths ' + var_pet_address_output.get() + '/temp_img.nii.gz -bin ' + var_pet_address_output.get() + \
            #  '/temp_img.nii.gz')
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_input.get() + \
             '/temp_img.nii.gz ' + var_pet_address_input.get() + '/PET_Cerebral_cortex.nii.gz ')

            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebral_cortex.nii.gz -M')
            L = len(x1)
            var_RA_refrence_mean = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebral_cortex.nii.gz -P 0')
            L = len(x1)
            var_RA_refrence_min = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebral_cortex.nii.gz -P 100')
            L = len(x1)
            var_RA_refrence_max = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Cerebral_cortex.nii.gz -S')
            L = len(x1)
            var_RA_reference_sd = x1[0:L-1]

        elif var_SUV_reference.get() == 'Pons':
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz' + ' -mul atlas_cortical/Pons.nii.gz ' + \
            var_pet_address_input.get() + '/PET_Pons.nii.gz')
            # os.system('fslmaths ' + var_pet_address_output.get() + '/temp_img.nii.gz -bin ' + var_pet_address_output.get() + \
            #  '/temp_img.nii.gz')
            # os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_output.get() + \
            #  '/temp_img.nii.gz ' + var_pet_address_output.get() + '/PET_Pons.nii.gz ')

            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Pons.nii.gz -M')
            L = len(x1)
            var_RA_refrence_mean = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Pons.nii.gz -P 0')
            L = len(x1)
            var_RA_refrence_min = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Pons.nii.gz -P 100')
            L = len(x1)
            var_RA_refrence_max = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_Pons.nii.gz -S')
            L = len(x1)
            var_RA_reference_sd = x1[0:L-1]

        elif var_SUV_reference.get() == 'Global gray matter':
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz' + ' -mul atlas_GE/global.nii.gz ' + \
            var_pet_address_input.get() + '/PET_global.nii.gz')
            # os.system('fslmaths ' + var_pet_address_output.get() + '/temp_img.nii.gz -bin ' + var_pet_address_output.get() + \
            #  '/temp_img.nii.gz')
            # os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_output.get() + \
            #  '/temp_img.nii.gz ' + var_pet_address_output.get() + '/PET_global.nii.gz ')

            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_global.nii.gz -M')
            L = len(x1)
            var_RA_refrence_mean = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_global.nii.gz -P 0')
            L = len(x1)
            var_RA_refrence_min = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_global.nii.gz -P 100')
            L = len(x1)
            var_RA_refrence_max = x1[0:L-1]
            status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_input.get() + '/PET_global.nii.gz -S')
            L = len(x1)
            var_RA_reference_sd = x1[0:L-1]


        os.system('echo ')
        os.system('echo ----------------ROI Analysis----------------')
        os.system('echo ')




        if var_atlas.get() == 'Harvard Oxford atlas':
            os.system('echo ---Calculating and saving SUV, SUVR, and cortical volume for 48 cortical areas according to the Harvard-Oxford atlas')


            # Measure SUV coefficient
            BMI = float(var_body_weight.get()) / (float(var_height.get()) * float(var_height.get()))

            if var_type_of_measurement.get() == 'Using body weight':
                x = (float(var_body_weight.get()) * 1000)
            elif var_type_of_measurement.get() == 'Using LBM (male)':
                x = (9270 * (float(var_body_weight.get()) * 1000)) / (6680 + (216*BMI))
            elif var_type_of_measurement.get() == 'Using LBM (female)':
                x = (9270 * (float(var_body_weight.get()) * 1000)) / (8780 + (244*BMI))

            coefficient = x / float(var_injected_dose.get())

            #Save SUV PET image for further visualization
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + str(coefficient) + ' ' + \
            var_pet_address_output.get() + '/SUV.nii.gz')

            #devide PET image by the reference mean to measure SUVR
            var_SUV_refrence_mean = float(var_RA_refrence_mean) / (float(var_injected_dose.get()) / x)
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -div ' + str(var_SUV_refrence_mean) + ' ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz')

            #Save SUVR PET image for further visualization
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz -mul ' + str(coefficient) + ' ' + \
            var_pet_address_output.get() + '/SUVR.nii.gz')


            for i in range (1,97):

                # Measure SUV
                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std -mul atlas_cortical/' + str(i) + '.nii.gz ' + \
                var_pet_address_output.get() + '/Cortical_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/Cortical_images/temp_img.nii.gz ' + var_pet_address_output.get() + '/Cortical_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/Cortical_images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz')


                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUV_cortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUV_cortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUV_cortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUV_cortical_sd = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_images/' + str(i) + '.nii.gz -V')
                L = len(x1)
                x2 = x1[0:L-1]
                var_ROI_cortical_volume = x2.rsplit(' ', 1)[1]



                file_SUV_cortical_mean = open(var_pet_address_output.get() + '/SUV_cortical_mean.txt', 'a')
                file_SUV_cortical_mean.write(str(var_SUV_cortical_mean))
                if i != 96:
                    file_SUV_cortical_mean.write('\n')
                file_SUV_cortical_mean.close()

                file_SUV_cortical_max = open(var_pet_address_output.get() + '/SUV_cortical_max.txt', 'a')
                file_SUV_cortical_max.write(str(var_SUV_cortical_max))
                if i != 96:
                    file_SUV_cortical_max.write('\n')
                file_SUV_cortical_max.close()

                file_SUV_cortical_min = open(var_pet_address_output.get() + '/SUV_cortical_min.txt', 'a')
                file_SUV_cortical_min.write(str(var_SUV_cortical_min))
                if i != 96:
                    file_SUV_cortical_min.write('\n')
                file_SUV_cortical_min.close()

                file_SUV_cortical_sd = open(var_pet_address_output.get() + '/SUV_cortical_sd.txt', 'a')
                file_SUV_cortical_sd.write(str(var_SUV_cortical_sd))
                if i != 96:
                    file_SUV_cortical_sd.write('\n')
                file_SUV_cortical_sd.close()

                file_cortical_volume = open(var_pet_address_output.get() + '/Cortical_volume.txt', 'a')
                file_cortical_volume.write(str(var_ROI_cortical_volume))
                if i != 96:
                    file_cortical_volume.write('\n')
                file_cortical_volume.close()



                # Measure SUVR

                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std -mul atlas_cortical/' + str(i) + '.nii.gz ' + \
                var_pet_address_output.get() + '/Cortical_normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/Cortical_normalized_images/temp_img.nii.gz ' + var_pet_address_output.get() + '/Cortical_normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/Cortical_normalized_images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz')

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUVR_cortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUVR_cortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUVR_cortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUVR_cortical_sd = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Cortical_normalized_images/' + str(i) + '.nii.gz -V')
                L = len(x1)
                x2 = x1[0:L-1]
                var_ROI_cortical_volume = x2.rsplit(' ', 1)[1]



                # var_SUVR_cortical_mean = float(var_RA_ROI_cortical_mean) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_max = float(var_RA_ROI_cortical_max) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_min = float(var_RA_ROI_cortical_min) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_sd = float(var_RA_ROI_cortical_sd)

                file_SUVR_cortical_mean = open(var_pet_address_output.get() + '/SUVR_cortical_mean.txt', 'a')
                file_SUVR_cortical_mean.write(str(var_SUVR_cortical_mean))
                if i != 96:
                    file_SUVR_cortical_mean.write('\n')
                file_SUVR_cortical_mean.close()

                file_SUVR_cortical_max = open(var_pet_address_output.get() + '/SUVR_cortical_max.txt', 'a')
                file_SUVR_cortical_max.write(str(var_SUVR_cortical_max))
                if i != 96:
                    file_SUVR_cortical_max.write('\n')
                file_SUVR_cortical_max.close()

                file_SUVR_cortical_min = open(var_pet_address_output.get() + '/SUVR_cortical_min.txt', 'a')
                file_SUVR_cortical_min.write(str(var_SUVR_cortical_min))
                if i != 96:
                    file_SUVR_cortical_min.write('\n')
                file_SUVR_cortical_min.close()

                file_SUVR_cortical_sd = open(var_pet_address_output.get() + '/SUVR_cortical_sd.txt', 'a')
                file_SUVR_cortical_sd.write(str(var_SUVR_cortical_sd))
                if i != 96:
                    file_SUVR_cortical_sd.write('\n')
                file_SUVR_cortical_sd.close()


            file1 = var_pet_address_output.get() + '/Areas_Cortical.txt'
            file2 = var_pet_address_output.get() + '/SUV_cortical_min.txt'
            file3 = var_pet_address_output.get() + '/SUV_cortical_max.txt'
            file4 = var_pet_address_output.get() + '/SUV_cortical_mean.txt'
            file5 = var_pet_address_output.get() + '/SUV_cortical_sd.txt'
            file6 = var_pet_address_output.get() + '/SUVR_cortical_min.txt'
            file7 = var_pet_address_output.get() + '/SUVR_cortical_max.txt'
            file8 = var_pet_address_output.get() + '/SUVR_cortical_mean.txt'
            file9 = var_pet_address_output.get() + '/SUVR_cortical_sd.txt'
            file10 = var_pet_address_output.get() + '/Cortical_volume.txt'
            file11 = var_pet_address_output.get() + '/temp_txt.txt'

            os.system('paste -d \' \' ' + file1 + ' ' + file2 + ' ' + file3 + ' ' + file4 + ' ' + file5 + ' '\
            + file6 + ' ' + file7 + ' ' + file8 + ' ' + file9 + ' ' + file10 + ' >> ' + file11)

            file12 = var_pet_address_output.get() + '/headers_cortical.txt'
            file13 = var_pet_address_output.get() + '/temp_txt.txt'
            file14 = var_pet_address_output.get() + '/OPETIA_cortical_all_info.txt'
            os.system('cat ' + file12 + ' ' + file13 + ' >> ' + file14)

            os.system('echo Done')




            os.system('echo ---Calculating and saving SUV, SUVR, and cortical volume for 19 subcortical areas according to the Harvard-Oxford atlas')

            BMI = float(var_body_weight.get()) / (float(var_height.get()) * float(var_height.get()))

            #devide PET image by the reference mean to measure SUVR
            var_SUV_refrence_mean = float(var_RA_refrence_mean) / (float(var_injected_dose.get()) / x)
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -div ' + str(var_SUV_refrence_mean) + ' ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz')

            for i in range (1,20):

                # Measure SUV coefficient

                if var_type_of_measurement.get() == 'Using body weight':
                    x = (float(var_body_weight.get()) * 1000)
                elif var_type_of_measurement.get() == 'Using LBM (male)':
                    x = (9270 * (float(var_body_weight.get()) * 1000)) / (6680 + (216*BMI))
                elif var_type_of_measurement.get() == 'Using LBM (female)':
                    x = (9270 * (float(var_body_weight.get()) * 1000)) / (8780 + (244*BMI))

                coefficient = x / float(var_injected_dose.get())

                # Measure SUV
                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std -mul atlas_subcortical/' + str(i) + '_* ' + \
                var_pet_address_output.get() + '/Subcortical_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/Subcortical_images/temp_img.nii.gz ' + var_pet_address_output.get() + '/Subcortical_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/Subcortical_images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz')


                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUV_subcortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUV_subcortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUV_subcortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUV_subcortical_sd = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_images/' + str(i) + '.nii.gz -V')
                L = len(x1)
                x2 = x1[0:L-1]
                var_ROI_subcortical_volume = x2.rsplit(' ', 1)[1]



                # var_SUV_subcortical_mean = float(var_RA_ROI_subcortical_mean) / (float(var_injected_dose.get()) / x)
                # var_SUV_subcortical_max = float(var_RA_ROI_subcortical_max) / (float(var_injected_dose.get()) / x)
                # var_SUV_subcortical_min = float(var_RA_ROI_subcortical_min) / (float(var_injected_dose.get()) / x)
                # var_SUV_subcortical_sd = float(var_RA_ROI_subcortical_sd)


                file_SUV_subcortical_mean = open(var_pet_address_output.get() + '/SUV_subcortical_mean.txt', 'a')
                file_SUV_subcortical_mean.write(str(var_SUV_subcortical_mean))
                if i != 19:
                    file_SUV_subcortical_mean.write('\n')
                file_SUV_subcortical_mean.close()

                file_SUV_subcortical_max = open(var_pet_address_output.get() + '/SUV_subcortical_max.txt', 'a')
                file_SUV_subcortical_max.write(str(var_SUV_subcortical_max))
                if i != 19:
                    file_SUV_subcortical_max.write('\n')
                file_SUV_subcortical_max.close()

                file_SUV_subcortical_min = open(var_pet_address_output.get() + '/SUV_subcortical_min.txt', 'a')
                file_SUV_subcortical_min.write(str(var_SUV_subcortical_min))
                if i != 19:
                    file_SUV_subcortical_min.write('\n')
                file_SUV_subcortical_min.close()

                file_SUV_subcortical_sd = open(var_pet_address_output.get() + '/SUV_subcortical_sd.txt', 'a')
                file_SUV_subcortical_sd.write(str(var_SUV_subcortical_sd))
                if i != 19:
                    file_SUV_subcortical_sd.write('\n')
                file_SUV_subcortical_sd.close()

                file_subcortical_volume = open(var_pet_address_output.get() + '/Subcortical_volume.txt', 'a')
                file_subcortical_volume.write(str(var_ROI_subcortical_volume))
                if i != 19:
                    file_subcortical_volume.write('\n')
                file_subcortical_volume.close()




                # Measure SUVR

                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std -mul atlas_subcortical/' + str(i) + '_* ' + \
                var_pet_address_output.get() + '/Subcortical_normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/Subcortical_normalized_images/temp_img.nii.gz ' + var_pet_address_output.get() + '/Subcortical_normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/Subcortical_normalized_images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz')


                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUVR_subcortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUVR_subcortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUVR_subcortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUVR_subcortical_sd = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/Subcortical_normalized_images/' + str(i) + '.nii.gz -V')
                L = len(x1)
                x2 = x1[0:L-1]
                var_ROI_subcortical_volume = x2.rsplit(' ', 1)[1]


                # var_SUVR_subcortical_mean = float(var_RA_ROI_subcortical_mean) / (float(var_injected_dose.get()) / x)
                # var_SUVR_subcortical_max = float(var_RA_ROI_subcortical_max) / (float(var_injected_dose.get()) / x)
                # var_SUVR_subcortical_min = float(var_RA_ROI_subcortical_min) / (float(var_injected_dose.get()) / x)
                # var_SUVR_subcortical_sd = float(var_RA_ROI_subcortical_sd)


                file_SUVR_subcortical_mean = open(var_pet_address_output.get() + '/SUVR_subcortical_mean.txt', 'a')
                file_SUVR_subcortical_mean.write(str(var_SUVR_subcortical_mean))
                if i != 19:
                    file_SUVR_subcortical_mean.write('\n')
                file_SUVR_subcortical_mean.close()

                file_SUVR_subcortical_max = open(var_pet_address_output.get() + '/SUVR_subcortical_max.txt', 'a')
                file_SUVR_subcortical_max.write(str(var_SUVR_subcortical_max))
                if i != 19:
                    file_SUVR_subcortical_max.write('\n')
                file_SUVR_subcortical_max.close()

                file_SUVR_subcortical_min = open(var_pet_address_output.get() + '/SUVR_subcortical_min.txt', 'a')
                file_SUVR_subcortical_min.write(str(var_SUVR_subcortical_min))
                if i != 19:
                    file_SUVR_subcortical_min.write('\n')
                file_SUVR_subcortical_min.close()

                file_SUVR_subcortical_sd = open(var_pet_address_output.get() + '/SUVR_subcortical_sd.txt', 'a')
                file_SUVR_subcortical_sd.write(str(var_SUVR_subcortical_sd))
                if i != 19:
                    file_SUVR_subcortical_sd.write('\n')
                file_SUVR_subcortical_sd.close()



            os.system('rm ' + var_pet_address_output.get() + '/temp_txt.txt')

            file1 = var_pet_address_output.get() + '/Areas_Subcortical.txt'
            file2 = var_pet_address_output.get() + '/SUV_subcortical_min.txt'
            file3 = var_pet_address_output.get() + '/SUV_subcortical_max.txt'
            file4 = var_pet_address_output.get() + '/SUV_subcortical_mean.txt'
            file5 = var_pet_address_output.get() + '/SUV_subcortical_sd.txt'
            file6 = var_pet_address_output.get() + '/SUVR_subcortical_min.txt'
            file7 = var_pet_address_output.get() + '/SUVR_subcortical_max.txt'
            file8 = var_pet_address_output.get() + '/SUVR_subcortical_mean.txt'
            file9 = var_pet_address_output.get() + '/SUVR_subcortical_sd.txt'
            file10 = var_pet_address_output.get() + '/Subcortical_volume.txt'
            file11 = var_pet_address_output.get() + '/temp_txt.txt'

            os.system('paste -d \' \' ' + file1 + ' ' + file2 + ' ' + file3 + ' ' + file4 + ' ' + file5 + ' '\
            + file6 + ' ' + file7 + ' ' + file8 + ' ' + file9 + ' ' + file10 + ' >> ' + file11)

            file12 = var_pet_address_output.get() + '/headers_subcortical.txt'
            file13 = var_pet_address_output.get() + '/temp_txt.txt'
            file14 = var_pet_address_output.get() + '/OPETIA_subcortical_all_info.txt'
            os.system('cat ' + file12 + ' ' + file13 + ' >> ' + file14)

            os.system('echo Done')


#--------------------------------------------------------------GE atlas



        elif var_atlas.get() == 'CortexID Suite atlas':

            os.system('echo ---Calculating and saving SUV, SUVR, and cortical volume for 26 areas according to the CortexID Suite atlas')


            # Measure SUV coefficient
            BMI = float(var_body_weight.get()) / (float(var_height.get()) * float(var_height.get()))

            if var_type_of_measurement.get() == 'Using body weight':
                x = (float(var_body_weight.get()) * 1000)
            elif var_type_of_measurement.get() == 'Using LBM (male)':
                x = (9270 * (float(var_body_weight.get()) * 1000)) / (6680 + (216*BMI))
            elif var_type_of_measurement.get() == 'Using LBM (female)':
                x = (9270 * (float(var_body_weight.get()) * 1000)) / (8780 + (244*BMI))

            coefficient = x / float(var_injected_dose.get())


            #Save SUV PET image for further visualization
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + str(coefficient) + ' ' + \
            var_pet_address_output.get() + '/SUV.nii.gz')


            #devide PET image by the reference mean to measure SUVR
            var_SUV_refrence_mean = float(var_RA_refrence_mean) / (float(var_injected_dose.get()) / x)
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -div ' + str(var_SUV_refrence_mean) + ' ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz')

            #Save SUV PET image for further visualization
            os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz -mul ' + str(coefficient) + ' ' + \
            var_pet_address_output.get() + '/SUVR.nii.gz')

            for i in range (1,27):



                # Measure SUV
                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std.nii.gz -mul atlas_GE/' + str(i) + '.nii.gz ' + \
                var_pet_address_output.get() + '/images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/images/temp_img.nii.gz ' + var_pet_address_output.get() + '/images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz')


                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUV_cortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUV_cortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUV_cortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUV_cortical_sd = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/images/' + str(i) + '.nii.gz -V')
                L = len(x1)
                x2 = x1[0:L-1]
                var_ROI_cortical_volume = x2.rsplit(' ', 1)[1]


                # var_SUV_cortical_mean = float(var_RA_ROI_cortical_mean) / (float(var_injected_dose.get()) / x)
                # var_SUV_cortical_max = float(var_RA_ROI_cortical_max) / (float(var_injected_dose.get()) / x)
                # var_SUV_cortical_min = float(var_RA_ROI_cortical_min) / (float(var_injected_dose.get()) / x)
                # var_SUV_cortical_sd = float(var_RA_ROI_cortical_sd)

                file_SUV_cortical_mean = open(var_pet_address_output.get() + '/SUV_mean.txt', 'a')
                file_SUV_cortical_mean.write(str(var_SUV_cortical_mean))
                if i != 26:
                    file_SUV_cortical_mean.write('\n')
                file_SUV_cortical_mean.close()

                file_SUV_cortical_max = open(var_pet_address_output.get() + '/SUV_max.txt', 'a')
                file_SUV_cortical_max.write(str(var_SUV_cortical_max))
                if i != 26:
                    file_SUV_cortical_max.write('\n')
                file_SUV_cortical_max.close()

                file_SUV_cortical_min = open(var_pet_address_output.get() + '/SUV_min.txt', 'a')
                file_SUV_cortical_min.write(str(var_SUV_cortical_min))
                if i != 26:
                    file_SUV_cortical_min.write('\n')
                file_SUV_cortical_min.close()

                file_SUV_cortical_sd = open(var_pet_address_output.get() + '/SUV_sd.txt', 'a')
                file_SUV_cortical_sd.write(str(var_SUV_cortical_sd))
                if i != 26:
                    file_SUV_cortical_sd.write('\n')
                file_SUV_cortical_sd.close()

                file_cortical_volume = open(var_pet_address_output.get() + '/volume.txt', 'a')
                file_cortical_volume.write(str(var_ROI_cortical_volume))
                if i != 26:
                    file_cortical_volume.write('\n')
                file_cortical_volume.close()



                # Measure SUVR

                os.system('fslmaths ' + var_pet_address_input.get() + '/graymatter_mask_std -mul atlas_GE/' + str(i) + '.nii.gz ' + \
                var_pet_address_output.get() + '/normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_input.get() + '/PET_brain_normalized_std.nii.gz -mul ' + var_pet_address_output.get() + \
                 '/normalized_images/temp_img.nii.gz ' + var_pet_address_output.get() + '/normalized_images/temp_img.nii.gz')
                os.system('fslmaths ' + var_pet_address_output.get() + '/normalized_images/temp_img.nii.gz -mul ' + str(coefficient) + \
                 ' ' + var_pet_address_output.get() + '/normalized_images/' + str(i) + '.nii.gz')


                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/normalized_images/' + str(i) + '.nii.gz -M')
                L = len(x1)
                var_SUVR_cortical_mean = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/normalized_images/' + str(i) + '.nii.gz -P 0')
                L = len(x1)
                var_SUVR_cortical_min = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/normalized_images/' + str(i) + '.nii.gz -P 100')
                L = len(x1)
                var_SUVR_cortical_max = x1[0:L-1]

                status, x1 = subprocess.getstatusoutput('fslstats ' + var_pet_address_output.get() + '/normalized_images/' + str(i) + '.nii.gz -S')
                L = len(x1)
                var_SUVR_cortical_sd = x1[0:L-1]



                BMI = float(var_body_weight.get()) / (float(var_height.get()) * float(var_height.get()))


                # var_SUVR_cortical_mean = float(var_RA_ROI_cortical_mean) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_max = float(var_RA_ROI_cortical_max) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_min = float(var_RA_ROI_cortical_min) / (float(var_injected_dose.get()) / x)
                # var_SUVR_cortical_sd = float(var_RA_ROI_cortical_sd)

                file_SUVR_cortical_mean = open(var_pet_address_output.get() + '/SUVR_mean.txt', 'a')
                file_SUVR_cortical_mean.write(str(var_SUVR_cortical_mean))
                if i != 26:
                    file_SUVR_cortical_mean.write('\n')
                file_SUVR_cortical_mean.close()

                file_SUVR_cortical_max = open(var_pet_address_output.get() + '/SUVR_max.txt', 'a')
                file_SUVR_cortical_max.write(str(var_SUVR_cortical_max))
                if i != 26:
                    file_SUVR_cortical_max.write('\n')
                file_SUVR_cortical_max.close()

                file_SUVR_cortical_min = open(var_pet_address_output.get() + '/SUVR_min.txt', 'a')
                file_SUVR_cortical_min.write(str(var_SUVR_cortical_min))
                if i != 26:
                    file_SUVR_cortical_min.write('\n')
                file_SUVR_cortical_min.close()

                file_SUVR_cortical_sd = open(var_pet_address_output.get() + '/SUVR_sd.txt', 'a')
                file_SUVR_cortical_sd.write(str(var_SUVR_cortical_sd))
                if i != 26:
                    file_SUVR_cortical_sd.write('\n')
                file_SUVR_cortical_sd.close()


            file1 = var_pet_address_output.get() + '/CortexID_areas.txt'
            file2 = var_pet_address_output.get() + '/SUV_min.txt'
            file3 = var_pet_address_output.get() + '/SUV_max.txt'
            file4 = var_pet_address_output.get() + '/SUV_mean.txt'
            file5 = var_pet_address_output.get() + '/SUV_sd.txt'
            file6 = var_pet_address_output.get() + '/SUVR_min.txt'
            file7 = var_pet_address_output.get() + '/SUVR_max.txt'
            file8 = var_pet_address_output.get() + '/SUVR_mean.txt'
            file9 = var_pet_address_output.get() + '/SUVR_sd.txt'
            file10 = var_pet_address_output.get() + '/volume.txt'
            file11 = var_pet_address_output.get() + '/temp_txt.txt'

            os.system('paste -d \' \' ' + file1 + ' ' + file2 + ' ' + file3 + ' ' + file4 + ' ' + file5 + ' '\
            + file6 + ' ' + file7 + ' ' + file8 + ' ' + file9 + ' ' + file10 + ' >> ' + file11)

            file12 = var_pet_address_output.get() + '/CortexID_headers.txt'
            file13 = var_pet_address_output.get() + '/temp_txt.txt'
            file14 = var_pet_address_output.get() + '/OPETIA_all_info.txt'
            os.system('cat ' + file12 + ' ' + file13 + ' >> ' + file14)

            os.system('echo Done')



        os.system('echo ')
        os.system('echo ----------Finish!')
        os.system('echo --------------------------------------------')
        os.system('echo ')




#___GUI
frame1 = LabelFrame(root, text='Input parameters', relief=SUNKEN, bd=2)
frame1.place(x=5, y=5, width=490, height=315)

Label(frame1, text="Folder including pre-processed data (OPETIA_output):").place(x=5, y=5)
Button(frame1, text="Browse", command=btn_enter_pet_input_command).place(x=5, y=30)
Entry(frame1, textvariable=var_pet_address_input).place(x=100, y=35, width=365)

Label(frame1, text="Output folder (name it ROI_analysis):").place(x=5, y=70)
Button(frame1, text="Browse", command=btn_enter_pet_output_command).place(x=5, y=95)
Entry(frame1, textvariable=var_pet_address_output).place(x=100, y=100, width=365)

Label(frame1, text="Tracer radioactivity (Bq):").place(x=5, y=140)
Entry(frame1, textvariable=var_injected_dose).place(x=365, y=140, width=100)

Label(frame1, text="Body weight (kg):").place(x=5, y=165)
Entry(frame1, textvariable=var_body_weight).place(x=365, y=165, width=100)

Label(frame1, text="Body height (m):").place(x=5, y=190)
Entry(frame1, textvariable=var_height).place(x=365, y=190, width=100)

Label(frame1, text='Type of measurement:').place(x=5, y=215)
ttk.Combobox(frame1, textvariable=var_type_of_measurement, values=['Using body weight', 'Using LBM (male)', 'Using LBM (female)'], state='readonly').place(x=265, y=220, width=200)

Label(frame1, text='SUV reference:').place(x=5, y=240)
ttk.Combobox(frame1, textvariable=var_SUV_reference, values=['Cerebellum', 'Cerebral cortex', 'Pons', 'Global gray matter'], state='readonly').place(x=265, y=245, width=200)

Label(frame1, text='Brain atlas:').place(x=5, y=265)
ttk.Combobox(frame1, textvariable=var_atlas, values=['Harvard Oxford atlas', 'CortexID Suite atlas'], state='readonly').place(x=265, y=270, width=200)

Button(root, text="Process", command=btn_process_command).place(x=5, y=325, width = 490)
Button(root, text="Open output folder", command=btn_open_folder_command).place(x=5, y=360, width = 490)

root.mainloop()