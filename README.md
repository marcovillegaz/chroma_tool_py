# ChromaToolPy - A Python Toolbox to Work with Chromatogram Data

![ChromatoPy Logo](Images/logo.png)  <!-- You can add a logo or image here -->

`ChromaToolPy` is a Python package designed to facilitate the analysis, processing, and visualization of chromatogram data. It provides tools for peak detection, baseline correction, integration, and more, to streamline chromatographic analysis workflows.

## Features

- Easy workflow employing classes
- Peak detection and characterization
- Baseline correction and normalization
- Integration of chromatographic peaks
- Visualization of chromatograms and results
- Data export for further analysis

# HPLC-signal-processng
This repository has usefull classes and methods for processing chromatogram data. All the scripts are based in the extractaed information from JASCO's ChromNAV software. The codes can be modified to process other type of information if it is in .txt

## Classes
### **Chromatogram** 
An instance of a Chromatogram classs is an object that contains all the information of a corresponding HPLC injection. This object can be created from PDA or FL detector data using the class methods (see chromatogram.py)

### **Analyte**
An instance of a Analyte class is an object that characterized a corresponding analyte. This class is useful to identify the compounds of interest using spectra information. 

* Create spectra library attribute. 

## Process ChromaNav peak information
When integrating peaks using ChromaNAV software, you can extract an excel file with the peak information ordered by channels in singles files. For example, CH1.xlsx store all the peaks in channel 1. 

### process_chromnav_batch.py (working)
take the chroman files rearrangen them as dataframe and load into and existing database, in this case a table. 

### merge_calibration_curve.py
Take a batch of chromnav files and merged the peak info with the concentration of each analites in each point. The scripts return an excel file where each sheet correspond to an analite. Then you can perform manaual analisis of the calibration curves. 











## post_processing
When you extract chromatogram information from ChromNav software, like peak area, peak name, etc. You can only extract one channel at a time. This gives you a group of excel files where each file represet the information of one channel of ther PDA detector. In this folder there are a bunch of scripts to postprocess this data. 

## utils.excel
Utility function to work with HPLC data in excel files.

## Order of the scripts.
In chromatography a private softaware (Usually develop by the brand) is use for
data aquisition and data processing. CHromatogram are basically one dimensional 
signals, where the response is an electric signal of the corresponding detector
(Diode Array Detector, Ultra Violete, Mass spectometer, absorbancia, among 
others). The advantages of python is to procces a great quantity of chromat

1. chroma_raname.py (ready)
    
2. merge_chanmels.py (ready)
    This function is ready and can be called in other scripts. The idea is to use 
    for multiple folders. In my case each folder is a different experiment.

3. chroma_corrector.py 

4. peak_integration.py

5. chroma-plots.py (semi-ready)
    This program can plot multiple chromatogram with many options. 

6. **cosmo_bar_plot.py** create a bar plot grouping the analytes by polymer tested, in order to compare the Ln(y). 



# chroma_display.py

chroma_plot.py contains function for different typo of visualizazarion of
chromatgram data. 

pda_contour(cls): Create contour plot from pda data (READY)
pda_2d(cls): Create a 2D chromatogram from your 3D PDA data  (READY)
