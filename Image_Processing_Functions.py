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
# Skull Stripping using ANTsPyNet
#------------------------------
def skull_strip(img_address, output_address, modality="t1"):

    # Load image
    img = ants.image_read(img_address)

    # Brain extraction
    # Modalities: "t1", "t2", "flair"
    brain_mask = antspynet.brain_extraction(img, modality)
    img_brain = img * brain_mask

    # Save the skull-stripped image
    ants.image_write(img_brain, output_address)

    return img_brain

#------------------------------
# Image Registration to MNI Space
#------------------------------
def register_to_MNI(img_address, output_address, registration_type="SyN"):

    # Working directory
    current_dir = os.getcwd()

    # Load images
    img = ants.image_read(img_address)
    MNI = ants.image_read(current_dir + "/Templates/MNI152_T1_2mm.nii.gz")

    # Perform registration (T1 → MNI)
    """
    registration_type:

    Linear (Rigid / Affine):
        "Translation" → Translation only (shifts)
        "Rigid" → Rigid-body (rotation + translation)
        "Similarity" → Rigid + uniform scaling
        "Affine" → Affine (rigid + scaling + shearing)
    
    Nonlinear (Deformable)
        "ElasticSyN" → Elastic deformation using SyN
        "SyN" → Symmetric normalization (nonlinear warp, very common for T1→MNI)
        "SyNOnly" → Just nonlinear deformation (no affine initialization)
        "SyNCC" → SyN using cross-correlation metric (good for intra-modality MRI)
        "SyNRA" → SyN with rigid + affine initialization
        "SyNAggro" → More aggressive version of SyN (stronger warps)
        "SyNabp" → SyN optimized for b0-dMRI → T1 registration
    """
    reg = ants.registration(
        fixed=MNI,        # target (MNI space)
        moving=img,        # source (subject T1)
        type_of_transform=registration_type
    )

    # Access the warped moving image (subject in MNI space)
    img_reg = reg["warpedmovout"]

    ants.image_write(img_reg, output_address)

    return img_reg

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