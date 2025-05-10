# OPETIA (Odense-Oxford PET Image Analysis)
![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/taha-parsayan/OPETIA?label=Release)
![Static Badge](https://img.shields.io/badge/Neuroimaging%20software-FF0000)
![Static Badge](https://img.shields.io/badge/Data%20Science-CC7722)
![Static Badge](https://img.shields.io/badge/Python-8A2BE2)
![Static Badge](https://img.shields.io/badge/FSL-8A2BE2)
![Static Badge](https://img.shields.io/badge/PET%20/%20MRI-4CAF50)


### Introduction
OPETIA is a user-friendly PET/MRI (Positron Emission Tomography / Magnetic Resonance Imaging) image analysis software, developed based on the [FSL](https://process.innovation.ox.ac.uk/software/p/9564/fslv5/1) software (Functional Magnetic Resonance Imaging of the Brain Software Library) and Python, for accurate brain image quantification. While FSL is widely used for MRI, OPETIA extends its functionality to PET imaging, offering a graphical user interface (GUI) to preprocess images and calculate SUV (Standardized Uptake Value) and SUVR (Standardized Uptake Value ratio) values. Image processing with OPETIA does not require users to have previous knowledge of medical image processing or programming since all the parameters for both MRI and PET image pre-processing are already set by default. At the same time, these parameters are provided in the GUI so that the users can modify them if needed.

The inputs of OPETIA include MRI T1-weighted, static PET, and the subject's information (body weight, height, total injected dose of the radiotracer).
The outputs of OPETIA include SUV & SUVR (min, mean, max, sd) and cortical volume (mean) of the regions of interest (ROI).
The Harvard-Oxford atlas with 48 cortical and 10 subcortical (including brain stem) ROIs have been selected as the default brain atlas for OPETIA. We have divided the regions into left and right hemispheres, resulting in 96 cortical and 19 subcortical ROIs.

![Image](https://github.com/user-attachments/assets/4de070b6-ad78-4c73-b657-43b7d3edcf65)

## Tools
OPETIA contains the following tools:
- MRIcroGL: for converting DICOM images to nifty images, and also for visualization.
- NIFTI organizer: For automatic data management. To copy all nifty images to their corresponding subject folders, and rename them to PET.nii and T1.nii
- Structural (MRI) image analysis
- Functional (PET) image analysis
- ROI analysis: to calculate SUV, SUVR, and cortical volume for 115 ROIs

The GUI of OPETIA is illustrated in the image below.

![GUI-figures](https://github.com/user-attachments/assets/e10b4fee-aeed-46f0-bb96-8a548b8c864f)

The pipeline of OPETIA is illustrated in the image below.

![pipeline](https://github.com/user-attachments/assets/d7997e20-9e5d-4655-8736-039365062f7a)

Statistical analysis showed a perfect alignment between the results of OPETIA and SPM12.

![Image](https://github.com/user-attachments/assets/852dbe5a-3b8b-4829-8c18-c3b2fc4179e1)

## How to use
### Initializations
OPETIA is running on Linux-based systems. First and foremost, the FSL needs to be installed using the following link:
[FSL installation](https://web.mit.edu/fsl_v5.0.10/fsl/doc/wiki/FslInstallation.html)

Next, download MRIcroGL_Linux from:
[MRIcroGL](https://www.nitrc.org/frs/?group_id=889)
Copy the file into the OPETIA folder and unzip it.

Next, the following initializations are required:
Ubuntu users:
- sudo apt-get update
- sudo apt install python3
- sudo apt-get install python3-tk
- sudo apt-get install eog
- module load FSL (for cloud-based servers, if necessary)

MacOS users:
- brew update
- brew install python@3.12
- brew install python-tk@3.12
(eog is not supported in MacOS)

### Usage example
To run OPETIA, create a folder and clone it to the OPETIA repository:
- git clone https://github.com/taha-parsayan/OPETIA.git

Next, open a terminal in the OPETIA folder and run the following command:
- python3 OPETIA.py

