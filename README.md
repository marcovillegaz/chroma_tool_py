# HPLC-signal-processng


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
