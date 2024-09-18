# OPETIA (Odense-Oxford PET Image Analysis)
![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/taha-parsayan/OPETIA?label=Release)
(https://img.shields.io/badge/any_text-you_like-blue)

### Introduction
OPETIA is a user-friendly PET/MRI (Positron EMission Tomography / Magnetic Resonance Imaging) image analysis toolbox, developed based on the [FSL](https://process.innovation.ox.ac.uk/software/p/9564/fslv5/1) software (Functional Magnetic Resonance Imaging of the Brain Software Library) and Python, for accurate brain image quantification. While FSL is widely used for MRI, OPETIA extends its functionality to PET imaging, offering a graphical user interface (GUI) to preprocess images and calculate SUV (Standardized Uptake Value) and SUVR (Standardized Uptake Value ratio) values. Image processing with OPETIA does not require the users to have previous knowledge of medical image processing or programming since all the parameter for both MRI and PET image pre-processings are already set as default. At the same time, these parameters are provided in the GUI so that the users can modify them if needed.

The inputs of OPETIA include MRI T1-weighted, static PET, and subject's information (body weight, height, total injected dose of the radiotracer).
The outputs of OPETIA include SUV & SUVR (min, mean, max, sd) and cortical volume (mean) of the regions of interest (ROI).
The Harvard-Oxford atlas with 48 cortical and 10 subcortical (including brain stem) ROIs have been selected as the default brain atlas for OPETIA. We have devided the regions into left and right hemispheres, resulting in 96 cortical nad 19 subcortical ROIs.



The GUI of OPETIA is illustrated in the image bellow.

![OPETIA](https://github.com/user-attachments/assets/d711c01f-1faf-49b8-85ac-4b31892b467d)

The pipeline of OPETIA is illustrated in the image bellow.

![pipeline](https://github.com/user-attachments/assets/d7997e20-9e5d-4655-8736-039365062f7a)

## How to use
### initializations
OPETIA is running on Linux-based systems. First and foremost, the FSL needs to be installed using the following link:
[FSL installation](https://web.mit.edu/fsl_v5.0.10/fsl/doc/wiki/FslInstallation.html)

Next, the following initializations are required:
- sudo apt-get update
- sudo apt install python2
- sudo apt-get install python-tk
- sudo apt-get install eog
- module load FSL

### Usage example
To run OPETIA, firstly create a folder and clone to the OPETIA repository:
- git clone https://github.com/taha-parsayan/OPETIA.git

Nex, open a terminal in the OPETIA folder and run the following command:
- python2 OPETIA.py

## Author Contributions
Mohammadtaha Parsayan: Software, Validation, Formal analysis, Investigation, Data Curation, Writing paper - Original Draft; Sasan Andalib: Writing paper - Review & Editing, Validation; Thomas Lund Andersen; Writing paper - Review & Editing, Methodology; Habib Ganjgahi; Writing paper -Review & Editing, Methodology; Poul Flemming Høilund-Carlsen; Writing paper - Review & Editing, Validation; Abass Alavi: Writing paper - Review & Editing, Validation; Mojtaba Zarei: Methodology, Conceptualization, Funding acquisition, Project administration, Validation, Writing paper - Review & Editing.
