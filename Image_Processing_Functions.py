"""
Functions for MRI Image Processing.
Author: Taha Parsayan
"""

import os
import numpy as np
import pandas as pd
import ants
import antspynet
import shutil
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

#------------------------------
# Skull Stripping using ANTsPyNet
#------------------------------
def skull_strip(img_address, output_brain_address, output_mask_address, modality):
    """
    Skull-strips an MRI image and saves both the brain and the mask.
    """
    img = ants.image_read(img_address)

    # Brain extraction
    # Modalities: "t1", "t2", "flair"
    brain_mask = antspynet.brain_extraction(img, modality)
    img_brain = img * brain_mask

    # Save skull-stripped image
    ants.image_write(img_brain, output_brain_address)

    # Save brain mask
    ants.image_write(brain_mask, output_mask_address)

#------------------------------
# Tissue Segmentation using Atropos
#------------------------------
def tissue_segmentation(img_address, brain_mask_address, output_address):
    """
    Segments brain tissues using Atropos. Uses an existing brain mask.
    """
    img = ants.image_read(img_address)
    img_n4 = ants.n4_bias_field_correction(img)

    brain_mask = ants.image_read(brain_mask_address)

    seg = ants.atropos(
        a=img_n4,
        x=brain_mask,           # Use existing brain mask
        i='kmeans[3]',          # 3 tissue classes: GM, WM, CSF
        m='[0.1,1x1x1]',        # smoothing
        c=5                     # max iterations
    )

    ants.image_write(seg['segmentation'], output_address)
    return seg['segmentation']


#------------------------------
# Split GM, WM, CSF from Segmentation
#------------------------------
def split_tissues(image_path, image_modality, segmented_path, out_dir, Registered):
    """
    Split a segmented T1 image into GM, WM, CSF masks.

    Parameters
    ----------
    segmented_path : str
        Path to segmented NIfTI file (e.g. T1_segmented.nii.gz).
    out_dir : str
        Directory where GM, WM, CSF images will be saved.
    """

    # Load the segmentation
    seg_img = nib.load(segmented_path)
    seg_data = seg_img.get_fdata() # labels: 1=CSF, 2=GM, 3=WM
    affine = seg_img.affine 
    header = seg_img.header

    # Define tissue labels
    tissue_labels = {
        "CSF": 1,
        "GM": 2,
        "WM": 3
    }

    # Create and save binary masks for each tissue
    for tissue, label in tissue_labels.items():
        tissue_mask = (seg_data == label).astype(np.uint8)
        tissue_img = nib.Nifti1Image(tissue_mask, affine, header)
        if Registered:
            out_path = os.path.join(out_dir, f"Mask_{image_modality}_{tissue}_MNI.nii.gz")
        else:
            out_path = os.path.join(out_dir, f"Mask_{image_modality}_{tissue}_native.nii.gz")
        nib.save(tissue_img, out_path)

    # Multiply masks by the original image to get tissue-specific images
    original_img = nib.load(image_path)
    original_data = original_img.get_fdata()
    if Registered:
        GM_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_GM_MNI.nii.gz")).get_fdata()
        WM_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_WM_MNI.nii.gz")).get_fdata()
        CSF_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_CSF_MNI.nii.gz")).get_fdata()
        GM = original_data * GM_mask
        WM = original_data * WM_mask
        CSF = original_data * CSF_mask
        nib.save(nib.Nifti1Image(GM, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_GM_MNI.nii.gz"))
        nib.save(nib.Nifti1Image(WM, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_WM_MNI.nii.gz"))
        nib.save(nib.Nifti1Image(CSF, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_CSF_MNI.nii.gz"))
    else:
        GM_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_GM_native.nii.gz")).get_fdata()
        WM_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_WM_native.nii.gz")).get_fdata()
        CSF_mask = nib.load(os.path.join(out_dir, f"Mask_{image_modality}_CSF_native.nii.gz")).get_fdata()

        GM = original_data * GM_mask
        WM = original_data * WM_mask
        CSF = original_data * CSF_mask
        nib.save(nib.Nifti1Image(GM, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_GM_native.nii.gz"))
        nib.save(nib.Nifti1Image(WM, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_WM_native.nii.gz"))
        nib.save(nib.Nifti1Image(CSF, original_img.affine, original_img.header), os.path.join(out_dir, f"{image_modality}_CSF_native.nii.gz"))


#------------------------------
# Image registration to MNI Space
#------------------------------
def register_to_MNI(img_address, output_image_address, registration_type="SyN"):
    """
    Registers an image to MNI space and saves:
    - The warped image
    - The transform files (affine + warp) as native_to_mni
    """

    img = ants.image_read(img_address)
    current_dir = os.getcwd()
    MNI = ants.image_read(os.path.join(current_dir, "Templates/MNI152_T1_2mm_brain.nii.gz"))

    reg = ants.registration(
        fixed=MNI,
        moving=img,
        type_of_transform=registration_type
    )

    # Save warped image
    img_reg = reg["warpedmovout"]
    ants.image_write(img_reg, output_image_address)

    # Save transforms
    affine_transform = reg['fwdtransforms'][1] if len(reg['fwdtransforms']) > 1 else reg['fwdtransforms'][0]
    warp_transform   = reg['fwdtransforms'][0] if len(reg['fwdtransforms']) > 1 else None

    output_folder = os.path.dirname(output_image_address)
    affine_out = os.path.join(output_folder, "native_to_mni_0GenericAffine.mat")
    shutil.copy(affine_transform, affine_out)

    if warp_transform:
        warp_out = os.path.join(output_folder, "native_to_mni_1Warp.nii.gz")
        shutil.copy(warp_transform, warp_out)


#------------------------------
# Apply Transform to Image
#------------------------------
def apply_transform_to_image(img_address, output_address, transform_list):
    """
    Applies a saved transform to an image.

    Parameters:
    - img_address: path to the moving image (e.g., segmentation in native space)
    - transform_list: list of transform file paths from registration (forward transforms)
    - output_address: path to save the transformed image
    - interpolation: interpolation method ('nearestNeighbor' for labels, 'linear' for intensity)
    """

    current_dir = os.getcwd()
    MNI_path = os.path.join(current_dir, "Templates/MNI152_T1_2mm_brain.nii.gz")

    # Load images
    fixed_img = ants.image_read(MNI_path)
    moving_img = ants.image_read(img_address)

    # Ensure transform_list is a list of strings (file paths)
    transform_list = [str(t) for t in transform_list]

    # Apply transforms
    img_transformed = ants.apply_transforms(
        fixed=fixed_img,
        moving=moving_img,
        transformlist=transform_list,
        interpolator='multiLabel')

    # Save the transformed image
    ants.image_write(img_transformed, output_address)
    
#------------------------------
# Visualize Image + overlay
#------------------------------

def plot_overlay(image1_path, image2_path, title):
    """
    Visualizes the registration result by overlaying contours of image1 on image2.
    Displays evenly spaced slices along the Z-axis.
    """
    # Load images
    fixed_img = nib.load(image1_path).get_fdata()
    moving_img = nib.load(image2_path).get_fdata()

    # Choose evenly spaced slices along Z axis
    num_slices = 30
    z_slices = np.linspace(0, fixed_img.shape[2]-1, num_slices, dtype=int)

    # Plot grid
    fig, axes = plt.subplots(5, 6, figsize=(8, 8))  # 3x4 grid
    axes = axes.flatten()
    fig.suptitle(title, fontsize=16)

    for i, z in enumerate(z_slices):
        fixed_slice = fixed_img[:, :, z]
        moving_slice = moving_img[:, :, z]

        axes[i].imshow(fixed_slice.T, cmap="gray", origin="lower")
        axes[i].contour(moving_slice.T, levels=[moving_slice.mean()], colors="red", linewidths=0.5)
        axes[i].set_title(f"Slice {z}")
        axes[i].axis("off")

    plt.tight_layout()
    plt.show()

#------------------------------
# Visualize One Image
#------------------------------import nibabel as nib

def plot_image(image_path, title, is_segmented=False):
    """
    Visualizes an MRI image by displaying evenly spaced slices along the Z-axis.
    For segmentation maps, uses FSL-like colors:
        1=CSF (blue), 2=GM (red), 3=WM (green)
    """
    # Load image
    img = nib.load(image_path).get_fdata()

    # Choose 12 evenly spaced slices along Z axis
    num_slices = 30
    z_slices = np.linspace(0, img.shape[2]-1, num_slices, dtype=int)

    # Plot grid
    fig, axes = plt.subplots(5, 6, figsize=(8, 8))  # 3x4 grid
    axes = axes.flatten()
    fig.suptitle(title, fontsize=16)

    # Define colormap if segmentation
    if is_segmented:
        # Map 0=black (background), 1=blue, 2=red, 3=green
        cmap = ListedColormap(["black", "blue", "red", "green"])
        bounds = np.arange(-0.5, 4.5)  # labels 0–3
        norm = BoundaryNorm(bounds, cmap.N)
    else:
        cmap = "gray"
        norm = None

    for i, z in enumerate(z_slices):
        slice_img = img[:, :, z]
        axes[i].imshow(slice_img.T, cmap=cmap, norm=norm, origin="lower")
        axes[i].set_title(f"Slice {z}")
        axes[i].axis("off")

    plt.tight_layout()
    plt.show()
