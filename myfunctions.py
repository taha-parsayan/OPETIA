from Tkinter import *
import os
import ttk
import tkFileDialog
from tkFileDialog import askopenfile


def get_address_file():
    file = tkFileDialog.askopenfile(mode='r', filetypes=[("All files", "*.nii"), ("All files", "*.gz")])

    if file:
        filepath = os.path.abspath(file.name)

    return filepath

def get_address_folder():
    file = tkFileDialog.askdirectory()

    return file

def get_address_file_reg_reference():
    default_path = '/opt/easybuild/software/FSL/6.0.3-foss-2019b-Python-3.7.4/fsl/data/standard/'
    file = tkFileDialog.askopenfile(initialdir=os.path.normpath(default_path), mode='r', filetypes=[("All files", "*.nii"), ("All files", "*.gz")])
    if file:
        filepath = os.path.abspath(file.name)
    return filepath


def get_address_file_reg_matrix(path):
    default_path = path
    file = tkFileDialog.askopenfile(initialdir=os.path.normpath(default_path), mode='r', filetypes=[("All files", "*.mat")])
    if file:
        filepath = os.path.abspath(file.name)
    return filepath


def FSL_Brain_Extraction(input, output, thr, func):
    if func == 'Standard brain extraction using bet2':
        bet_option = ' '
    elif func == 'Robust brain centre estimation':
        bet_option = '-R'
    elif func == 'Eye & optic nerve cleanup':
        bet_option = '-S'
    elif func == 'Bias field & neck cleanup':
        bet_option = '-B'
    elif func == 'Improve BET if FOV is very small in Z':
        bet_option = '-Z'
    elif func == 'Apply to 4D FMRI data':
        bet_option = '-F'
    elif func == 'Run bet2 and then betsurf to get additional skull and scalp surfaces':
        bet_option = '-A'
    elif func == 'As above, when also feeding in non-brain-extracted T2':
        bet_option = '-A2'
    os.system('bet '+ input + ' ' + output + ' ' + '-f ' + thr + ' ' + bet_option)


def register_flirt(input, output, ref, model, matrix_name, cost_f, interp):
    if model == 'Translation only - 3DOF':
        DOF = 3
    elif model == 'Rigid body - 6DOF':
        DOF = 6
    elif model == 'Gloval rescale - 7DOF':
        DOF = 7
    elif model == 'Traditional - 9DOF':
        DOF = 9
    elif model == 'Affine - 12DOF':
        DOF = 12

    if cost_f == 'Correlation ratio':
        cost_func = 'corratio'
    elif cost_f == 'Mutual information':
        cost_func = 'mutualinfo'
    elif cost_f == 'Normalised mutual information':
        cost_func = 'normmi'
    elif cost_f == 'Normalised correlation':
        cost_func = 'normcorr'
    elif cost_f == 'Least squares':
        cost_func = 'leastsq'

    if interp == 'Tri-linear':
        interpol = 'trilinear'
    elif interp == 'Nearest neighbour':
        interpol = 'nearestneighbour'
    elif interp == 'Spline':
        interpol = 'spline'
    elif interp == 'Sinc':
        interpol = 'sinc'

    os.system('flirt -in ' + input + ' -ref ' + ref + ' -out ' + output + ' ' +' -omat ' + matrix_name + ' '
     + '-bins 256 -cost ' + cost_func + ' -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp ' + interpol)



def register_using_matrix(input, output, mat, ref):
    os.system('flirt -in ' + input + ' -applyxfm ' + '-init ' + mat + ' -out ' + output + ' ' + ' -paddingsize 0.0 -interp trilinear ' +
    '-ref ' + ref )


def FSL_FAST(input, output):
    os.system('fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o ' + output + '/fast' + ' ' + input)
