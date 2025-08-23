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
# Image Registration
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

# img_address = "/Users/taha/Desktop/ADNI/033_S_0920/T1.nii.gz"
# img_dir = os.path.dirname(img_address)
# output_address = os.path.join(img_dir, "OPETIA_output", "T1_std.nii.gz")
# reg = ipf.register_to_MNI(img_address, output_address)



T1 = ants.image_read("/Users/taha/Desktop/ADNI/033_S_0920/OPETIA_output/T1_std.nii.gz")
brain_mask = antspynet.brain_extraction(T1, modality="t1")
T1_brain = T1 * brain_mask
ants.plot(T1_brain)

# Optional: Save the skull-stripped image
ants.image_write(T1_brain, "/Users/taha/Desktop/ADNI/033_S_0920/T1_brain.nii.gz")


T1_brain_n4 = ants.n4_bias_field_correction(T1_brain)


seg = ants.atropos(
    a=T1_brain_n4,
    x=brain_mask,           # Use brain mask to restrict segmentation
    i='kmeans[3]',          # 3 tissue classes
    m='[0.1,1x1x1]',        # smoothing
    c=5                     # max iterations
)

# seg['segmentation'] contains labeled image: 1=CSF, 2=GM, 3=WM
ants.plot(T1_brain_n4, seg['segmentation'])
ants.image_write(seg['segmentation'], "/Users/taha/Desktop/ADNI/033_S_0920/T1_seg.nii.gz")

