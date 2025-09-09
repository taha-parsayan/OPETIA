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
import fnmatch
import math
import glob

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
# Image co-registration
#------------------------------
def co_registration(img_address, ref_address, output_image_address, registration_type="Rigid"):
    """
    Co-registers an image to another image
    """

    # Define linear and nonlinear types
    # linear_types = {"Translation", "Rigid", "Similarity", "Affine"}
    # nonlinear_types = {"SyN", "ElasticSyN", "SyNOnly", "SyNCC", "SyNRA", "SyNAggro", "SyNabp"}

    img = ants.image_read(img_address)
    ref = ants.image_read(ref_address)

    reg = ants.registration(
        fixed=ref,
        moving=img,
        type_of_transform="Rigid"
    )

    # Save warped image
    img_reg = reg["warpedmovout"]
    ants.image_write(img_reg, output_image_address)


#------------------------------
# Adding coregistered PET volumes to make a static
#------------------------------
def add_PET_vols(path):
    """
    Adds all PET dynamic volumes in a folder to create a static volume.
    """

    # Find and sort PET volumes
    PET_volumes = sorted(fnmatch.filter(os.listdir(path), 'vol*_coreg.nii.gz'))

    if not PET_volumes:
        raise ValueError("No PET volumes found in the folder!")

    # Read first image to initialize sum
    static_vol = ants.image_read(os.path.join(path, PET_volumes[0]))

    # Add remaining volumes
    for vol_name in PET_volumes[1:]:
        img = ants.image_read(os.path.join(path, vol_name))
        static_vol += img  # element-wise addition

    # Save static PET volume
    ants.image_write(static_vol, os.path.join(path, "pet_coreg.nii.gz"))


#------------------------------
# Applying a mask to an image
#------------------------------
def apply_mask(image_path, mask_path, output_path):
    """
    Apply a binary mask to an image and save the result.

    Parameters:
    - image_path: path to input image (.nii or .nii.gz)
    - mask_path: path to binary mask (.nii or .nii.gz)
    - output_path: path to save masked image
    """
    # Load image and mask
    img = ants.image_read(image_path)
    mask = ants.image_read(mask_path)

    # Multiply image by mask
    img_masked = img * mask

    # Save masked image
    ants.image_write(img_masked, output_path)


#------------------------------
# Image registration to MNI Space
#------------------------------
def register_to_MNI(img_address, output_image_address, registration_type="SyN", save_matrix=True):
    """
    Registers an image to MNI space and saves:
    - The warped image
    - The transform files (affine + optional warp) as native_to_mni
    """

    # Define linear and nonlinear types
    linear_types = {"Translation", "Rigid", "Similarity", "Affine"}
    nonlinear_types = {"SyN", "ElasticSyN", "SyNOnly", "SyNCC", "SyNRA", "SyNAggro", "SyNabp"}

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
    if save_matrix:
        output_folder = os.path.dirname(output_image_address)

        if registration_type in linear_types:
            # Only affine transform
            affine_transform = reg['fwdtransforms'][0]
            affine_out = os.path.join(output_folder, "native_to_mni_0GenericAffine.mat")
            shutil.copy(affine_transform, affine_out)

        elif registration_type in nonlinear_types:
            # Nonlinear → warp + affine
            # Order in fwdtransforms: [warp, affine]
            warp_transform   = reg['fwdtransforms'][0]
            affine_transform = reg['fwdtransforms'][1]

            warp_out = os.path.join(output_folder, "native_to_mni_1Warp.nii.gz")
            affine_out = os.path.join(output_folder, "native_to_mni_0GenericAffine.mat")

            shutil.copy(warp_transform, warp_out)
            shutil.copy(affine_transform, affine_out)

#------------------------------
# Apply Transform to Image
#------------------------------
def apply_transform_to_image(img_address, output_address, transform_list, interpolation='multiLabel'):
    """
    Applies saved transform(s) to an image (works for both linear and nonlinear registrations).

    Parameters:
    - img_address: path to the moving image (e.g., segmentation in native space)
    - transform_list: list of transform file paths from registration (forward transforms)
                      should be in ANTs fwdtransforms order: [warp (if any), affine]
    - output_address: path to save the transformed image
    - interpolation: 'multiLabel' for label maps, 'linear' for intensity images
    """

    current_dir = os.getcwd()
    MNI_path = os.path.join(current_dir, "Templates/MNI152_T1_2mm_brain.nii.gz")

    # Load images
    fixed_img = ants.image_read(MNI_path)
    moving_img = ants.image_read(img_address)

    # Ensure transform_list is a list of strings
    if isinstance(transform_list, str):
        transform_list = [transform_list]
    else:
        transform_list = [str(t) for t in transform_list]

    # Apply transforms
    img_transformed = ants.apply_transforms(
        fixed=fixed_img,
        moving=moving_img,
        transformlist=transform_list,
        interpolator=interpolation
    )

    # Save the transformed image
    ants.image_write(img_transformed, output_address)


#------------------------------
# Smoothing an Image
#------------------------------

def smooth_image(input_path, output_path, fwhm=5):
    # Read image
    img = ants.image_read(input_path)
    
    # Convert FWHM to sigma (σ = FWHM / 2.355)
    sigma = fwhm / 2.355
    
    # Smooth
    smoothed_img = ants.smooth_image(img, sigma=sigma, sigma_in_physical_coordinates=True)
    
    # Save
    ants.image_write(smoothed_img, output_path)


#------------------------------
# Splitting Dynanic PET Into Volumes
#------------------------------


def split_dynamic_pet(input_path, output_dir, prefix="vol"):
    """
    Split a 4D dynamic PET NIfTI file into multiple 3D volumes,
    preserving the original affine and header for alignment.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load the 4D PET image
    img = nib.load(input_path)
    data = img.get_fdata() # converts the NIfTI image into a NumPy array
    affine = img.affine # The affine matrix is a 4×4 matrix that maps voxel coordinates to real-world coordinates (usually in millimeters)
    header = img.header # The header contains metadata about the image

    # Check if the image is 4D
    if len(data.shape) != 4:
        # Only one volume, save as vol0000
        output_path = os.path.join(output_dir, "vol0000.nii.gz")
        nib.save(nib.Nifti1Image(data, affine, header), output_path)
        return

    # Split into frames
    for t in range(data.shape[3]):
        vol_data = data[..., t]  # extract 3D frame
        output_path = os.path.join(output_dir, f"{prefix}{t:04d}.nii.gz")
        # Use original affine and header to preserve alignment
        nib.save(nib.Nifti1Image(vol_data, affine, header), output_path)

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
#------------------------------

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

#------------------------------
# Visualize Three Images
#------------------------------

def plot_3_images_overlay(img1_path, img2_path, img3_path, title, num_slices=30):
    """
    Visualizes 3 MRI/PET images overlaid in RGB colors on evenly spaced slices.
    - img1 → Red
    - img2 → Green
    - img3 → Blue

    Rotates each slice 90 degrees for proper brain orientation.
    """

    # Load images
    img1 = nib.load(img1_path).get_fdata()
    img2 = nib.load(img2_path).get_fdata()
    img3 = nib.load(img3_path).get_fdata()

    # Ensure same shape
    if not (img1.shape == img2.shape == img3.shape):
        raise ValueError(f"All images must have the same shape! Got {img1.shape}, {img2.shape}, {img3.shape}")

    # Reorder axes if needed so last dimension is Z (slices)
    if img1.shape[2] < img1.shape[0] and img1.shape[2] < img1.shape[1]:
        img1 = np.transpose(img1, (1, 2, 0))
        img2 = np.transpose(img2, (1, 2, 0))
        img3 = np.transpose(img3, (1, 2, 0))

    # Determine which slices to show along Z
    z_slices = np.linspace(0, img1.shape[2] - 1, min(num_slices, img1.shape[2]), dtype=int)

    # Compute grid layout
    n_slices = len(z_slices)
    n_cols = min(6, n_slices)
    n_rows = math.ceil(n_slices / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(8, 8))
    axes = axes.flatten()
    fig.suptitle(title, fontsize=16)

    # Normalize helper
    def normalize(slice):
        slice_min = slice.min()
        slice_max = slice.max()
        return (slice - slice_min) / (slice_max - slice_min + 1e-8)

    for i, z in enumerate(z_slices):
        slice1 = img1[:, :, z]
        slice2 = img2[:, :, z]
        slice3 = img3[:, :, z]

        # Stack into RGB (R=img1, G=img2, B=img3)
        rgb_slice = np.stack([normalize(slice1),
                              normalize(slice2),
                              normalize(slice3)], axis=-1)

        # Rotate 90 degrees
        rgb_slice_rot = np.rot90(rgb_slice, k=3) # 270 degree rotation

        axes[i].imshow(rgb_slice_rot, origin="lower")
        axes[i].set_title(f"Slice {z}")
        axes[i].axis("off")

    # Turn off unused axes
    for ax in axes[n_slices:]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()

#------------------------------
# Segmentation of ROIs - Harvard-Oxford Atlas
#------------------------------
def ROI_segmentation_Harvard_Oxford(image_path, output_path, image_modality = "MRI"):
    """
    Applying Harvard-Oxford atlas ROI masks into an image

    Parameters:
    - image: MRI Gray Matter or PET Gray Matter
    - output_path: ROI_Analysis
    - image_modality: MRI or PET
    """

    current_dir = os.getcwd()
    # Path to the ROI masks
    cortical_ROIs_dir = os.path.join(current_dir, "atlas_cortical")
    subcortical_ROIs_dir = os.path.join(current_dir, "atlas_subcortical")

    # Read the image
    image = ants.image_read(image_path)
    
    # Applying subcortical masks
    for i in range(1, 20):
        pattern = os.path.join(subcortical_ROIs_dir, f"{i}_*.nii.gz")
        matches = glob.glob(pattern)
        if not matches:
            raise FileNotFoundError(f"No ROI mask found for pattern: {pattern}")
        roi_path = matches[0]
        ROI_mask = ants.image_read(roi_path) # ROI mask from atlas
        ROI = image * ROI_mask # ROI
        out_path = os.path.join(output_path, f"{image_modality}_Subcortical_ROIs", f"{i}.nii.gz")
        ants.image_write(ROI, out_path)

    # Applying cortical masks
    for i in range(1, 97):
        pattern = os.path.join(cortical_ROIs_dir, f"{i}.nii.gz")
        matches = glob.glob(pattern)
        if not matches:
            raise FileNotFoundError(f"No ROI mask found for pattern: {pattern}")
        roi_path = matches[0]
        ROI_mask = ants.image_read(roi_path) # ROI mask from atlas
        ROI = image * ROI_mask # ROI
        out_path = os.path.join(output_path, f"{image_modality}_Cortical_ROIs", f"{i}.nii.gz")
        ants.image_write(ROI, out_path)

#------------------------------
# Calculate volume from MRI
#------------------------------
def calculate_mri_volume(file_path, threshold=0):
    """
    Calculate the volume of an MRI image (or mask) in mm^3.

    Parameters:
    - file_path: str, path to the NIfTI image
    - threshold: float, voxel intensity threshold to count as "inside" (default=0)

    Returns:
    - total_volume_mm3: float, volume in cubic millimeters
    """
    # Load image
    img = ants.image_read(file_path)
    
    # Get voxel spacing and volume
    voxel_spacing = img.spacing
    voxel_volume = np.prod(voxel_spacing)  # in mm^3

    # Get data array
    data = img.numpy()
    
    # Count voxels above threshold
    n_voxels = (data > threshold).sum()
    
    # Calculate total volume in mm^3
    total_volume_mm3 = n_voxels * voxel_volume
    
    return total_volume_mm3


#------------------------------
# Calculate SUVR from PET
#------------------------------
def calculate_suvr(ROI_path, reference_path):
    """
    Calculate SUVR (Standardized Uptake Value Ratio) from a PET image.

    Parameters:
    - ROI_path: str, path to ROI mask (binary NIfTI)
    - reference_path: str, path to reference region mask (binary NIfTI)

    Returns:
    - SUVR_mean, SUVR_max, SUVR_min (floats)
    """
    import ants
    import numpy as np

    # Load ROI and reference masks
    ROI = ants.image_read(ROI_path).numpy()
    ref = ants.image_read(reference_path).numpy()

    # Extract voxel values (ignore background 0s)
    ROI_data = ROI[ROI > 0]
    ref_data = ref[ref > 0]

    # Calculate SUV values
    SUV_mean = float(np.mean(ROI_data))
    SUV_max = float(np.max(ROI_data))
    SUV_min = float(np.min(ROI_data))

    ref_mean = float(np.mean(ref_data))

    # Calculate SUVR (ROI / reference)
    SUVR_mean = SUV_mean / ref_mean
    SUVR_max = SUV_max / ref_mean
    SUVR_min = SUV_min / ref_mean

    return SUVR_mean, SUVR_max, SUVR_min



