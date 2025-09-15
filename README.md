# OPETIA (Odense-Oxford PET Image Analysis)
![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/taha-parsayan/OPETIA?label=Release)
![Static Badge](https://img.shields.io/badge/Neuroimaging%20software-FF0000)
![Static Badge](https://img.shields.io/badge/Data%20Science-CC7722)
![Static Badge](https://img.shields.io/badge/Python-8A2BE2)
![Static Badge](https://img.shields.io/badge/FSL-8A2BE2)
![Static Badge](https://img.shields.io/badge/PET%20/%20MRI-4CAF50)


### Introduction
OPETIA is a user-friendly PET/MRI (Positron Emission Tomography / Magnetic Resonance Imaging) image analysis software, developed using Python for accurate brain image quantification.

OPETIA can be run on:
- Windows
- Linux Ubuntu
- MacOS

OPETIA offers a graphical user interface (GUI) to process images and calculate cerebral volume from MRI images and SUVR (Standardized Uptake Value ratio) from PET images. Image processing with OPETIA does not require users to have previous knowledge of medical image processing or programming since all the parameters for both MRI and PET image pre-processing are already set by default. At the same time, these parameters are provided in the GUI so that the users can modify them if needed.

The inputs of OPETIA include MRI T1-weighted and dynamic PET.
The outputs of OPETIA include SUVR (min, mean, max) and cortical volume (mean) of the regions of interest (ROI).
The Harvard-Oxford atlas with 48 cortical and 10 subcortical (including brain stem) ROIs have been selected as the default brain atlas for OPETIA. I have divided the regions into left and right hemispheres, resulting in 96 cortical and 19 subcortical ROIs.

<img width="1470" height="838" alt="Image" src="https://github.com/user-attachments/assets/7cc2fd2d-fdbd-42b5-9241-a0df342ffbe0" />
<img width="1470" height="830" alt="Image" src="https://github.com/user-attachments/assets/e3646ae6-ecca-4375-bd0a-4b4fa4d12ec8" />
<img width="719" height="472" alt="Image" src="https://github.com/user-attachments/assets/b8bfa2f4-1327-4859-a873-94565e9f0559" />

## Tools
OPETIA contains the following tools:
- MRIcroGL: for converting DICOM images to nifty images, and also for visualization.
- Structural (MRI) image processing
- Functional (PET) image processing (static or dynamic)
- ROI analysis: to calculate SUVR and cortical volume for 115 ROIs

Every tool within OPETIA is provided with the flowchart of the data processing, including the input data and the output data.
Additionally, the log box within OPETIA prints the data processing stages for monitoring and error handling.

## How to Use OPETIA

### 1. Download OPETIA

1. Install **Conda** from the official website: [ANACONDA](https://www.anaconda.com/download)
   (Choose Miniconda for your OS: Windows, macOS, or Linux.)
2. Open a terminal (macOS and Linux) or Anaconda Prompt (Windows) and run:

```bash
conda --version 
```

To make sure Conda is installed successfully.

Then get OPETIA by running:

```bash
git clone https://github.com/taha-parsayan/OPETIA.git
cd OPETIA
```

---

### 2. Create Conda Environment, Install Packages, and Run OPETIA

#### All Platforms (Windows / macOS / Linux)

1. **Create the Conda environment (only on time)**:

```bash
conda env create -f environment.yml
```

2. **Run OPETIA**:

```bash
conda activate opetia
python OPETIA.py
```

---

### Notes

* The Conda environment includes Python 3.12 and all required packages (`numpy`, `pandas`, `matplotlib`, `nibabel`, `antspyx`, `antspynet`, `customtkinter`, etc.).
* On macOS with M1/M2, TensorFlow will use the `tensorflow-macos` + `tensorflow-metal` stack for hardware acceleration.

## Citation
Please cite the following paper:
https://www.sciencedirect.com/science/article/pii/S1053811925002812
