# HPLC-signal-processng
This repository has usefull classes and methods for processing chromatogram data. All the scripts are based in the extractaed information from JASCO's ChromNAV software

## Classes
### **Chromatogram** 
An instance of a Chromatogram classs is an object that contains all the information of a corresponding HPLC injection. This object can be created from PDA or FL detector data using the class methods (see chromatogram.py)

### **Analyte**
An instance of a Analyte class is an object that characterized a corresponding analyte. This class is useful to identify the compounds of interest using spectra information. 

* Create spectra library attribute. 

## Process peak information
When integrating peaks using ChromaNAV software, you can extract an excel file with the peak information ordered by channels in singles files. For example, CH1.xlsx store all the peaks 


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
