"""
ROI Analysis Panel for OPETIA:

This pipeline segments both MRI and PET images into ROIs
and extracts volume, SUV, and SUVR for every region.

The output is saved as a .csv file.

Author: Taha Parsayan
"""

#------------------------------
# Import Libraries
#------------------------------
import os
import sys
import time
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import Image_Processing_Functions as ipf
import threading

# ------------------------------
# Main class
# ------------------------------

class ROIpanel:
    def __init__(self, parent):
        self.parent = parent
        self._setup_variables()
        self._build_gui()
    
    # -------------------------------
    # Variables
    # -------------------------------
    def _setup_variables(self):
        pass

    # -------------------------------
    # GUI Layout
    # -------------------------------
    def _build_gui(self):
        pass

