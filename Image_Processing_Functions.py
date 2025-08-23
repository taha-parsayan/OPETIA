"""
Functions for MRI Image Processing.
Author: Taha Parsayan
"""

import os
import numpy as np
import pandas as pd
import ants
import antspynet

#------------------------------
# Image Registration to MNI Space
#------------------------------
def register_to_MNI(img_address, output_address):

    # Working directory
    current_dir = os.getcwd()

    # Load images
    img = ants.image_read(img_address)
    MNI = ants.image_read(current_dir + "/Templates/MNI152_T1_2mm.nii.gz")

    # Perform registration (T1 → MNI)
    reg = ants.registration(
        fixed=MNI,        # target (MNI space)
        moving=img,        # source (subject T1)
        type_of_transform="SyN"   # nonlinear transform (symmetric normalization)
    )

    # Access the warped moving image (subject in MNI space)
    img_reg = reg["warpedmovout"]

    ants.image_write(img_reg, output_address)

    return img_reg

#------------------------------
# Skull Stripping using ANTsPyNet
#------------------------------
def skull_strip(img_address, output_address):

    # Load image
    img = ants.image_read(img_address)

    # Brain extraction
    brain_mask = antspynet.brain_extraction(img, modality="t1")
    img_brain = img * brain_mask

    # Save the skull-stripped image
    ants.image_write(img_brain, output_address)

    return img_brain

#------------------------------
# Tissue Segmentation using Atropos
#------------------------------
def tissue_segmentation(img_address, output_address):

    # Load image
    img = ants.image_read(img_address)

    # N4 Bias Field Correction
    img_n4 = ants.n4_bias_field_correction(img)

    # Brain extraction to get brain mask
    brain_mask = antspynet.brain_extraction(img, modality="t1")

    # Tissue segmentation using Atropos
    seg = ants.atropos(
        a=img_n4,
        x=brain_mask,           # Use brain mask to restrict segmentation
        i='kmeans[3]',          # 3 tissue classes
        m='[0.1,1x1x1]',        # smoothing
        c=5                     # max iterations
    )

    # Save the segmentation result
    ants.image_write(seg['segmentation'], output_address)

    return seg['segmentation']