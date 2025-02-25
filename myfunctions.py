from tkinter import *
from tkinter import ttk, filedialog
import os


def get_address_file():
    file = filedialog.askopenfile(mode='r', filetypes=[("NIfTI files", "*.nii"), ("Compressed NIfTI files", "*.gz")])
    if file:
        return os.path.abspath(file.name)
    return None


def get_address_folder():
    return filedialog.askdirectory()


def get_address_file_reg_reference():
    default_path = '/opt/easybuild/software/FSL/6.0.3-foss-2019b-Python-3.7.4/fsl/data/standard/'
    file = filedialog.askopenfile(initialdir=os.path.normpath(default_path), mode='r', filetypes=[("NIfTI files", "*.nii"), ("Compressed NIfTI files", "*.gz")])
    if file:
        return os.path.abspath(file.name)
    return None


def get_address_file_reg_matrix(path):
    file = filedialog.askopenfile(initialdir=os.path.normpath(path), mode='r', filetypes=[("Matrix files", "*.mat")])
    if file:
        return os.path.abspath(file.name)
    return None


def FSL_Brain_Extraction(input_file, output, thr, func):
    bet_options = {
        'Standard brain extraction using bet2': '',
        'Robust brain centre estimation': '-R',
        'Eye & optic nerve cleanup': '-S',
        'Bias field & neck cleanup': '-B',
        'Improve BET if FOV is very small in Z': '-Z',
        'Apply to 4D FMRI data': '-F',
        'Run bet2 and then betsurf to get additional skull and scalp surfaces': '-A',
        'As above, when also feeding in non-brain-extracted T2': '-A2'
    }
    
    bet_option = bet_options.get(func, '')
    os.system(f'bet {input_file} {output} -f {thr} {bet_option}')


def register_flirt(input_file, output, ref, model, matrix_name, cost_f, interp):
    dof_options = {
        'Translation only - 3DOF': 3,
        'Rigid body - 6DOF': 6,
        'Global rescale - 7DOF': 7,
        'Traditional - 9DOF': 9,
        'Affine - 12DOF': 12
    }
    
    cost_func_options = {
        'Correlation ratio': 'corratio',
        'Mutual information': 'mutualinfo',
        'Normalised mutual information': 'normmi',
        'Normalised correlation': 'normcorr',
        'Least squares': 'leastsq'
    }
    
    interp_options = {
        'Tri-linear': 'trilinear',
        'Nearest neighbour': 'nearestneighbour',
        'Spline': 'spline',
        'Sinc': 'sinc'
    }
    
    dof = dof_options.get(model, 12)
    cost_func = cost_func_options.get(cost_f, 'corratio')
    interpol = interp_options.get(interp, 'trilinear')

    os.system(f'flirt -in {input_file} -ref {ref} -out {output} -omat {matrix_name} '
              f'-bins 256 -cost {cost_func} -searchrx -90 90 -searchry -90 90 -searchrz -90 90 '
              f'-dof {dof} -interp {interpol}')


def register_using_matrix(input_file, output, mat, ref):
    os.system(f'flirt -in {input_file} -applyxfm -init {mat} -out {output} -paddingsize 0.0 -interp trilinear -ref {ref}')


def FSL_FAST(input_file, output):
    os.system(f'fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o {output}/fast {input_file}')
