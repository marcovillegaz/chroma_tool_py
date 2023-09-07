# HPLC-signal-processng


## Order of the scripts.

In chromatography a private softaware (Usually develop by the brand) is use for
data aquisition and data processing. CHromatogram are basically one dimensional 
signals, where the response is an electric signal of the corresponding detector
(Diode Array Detector, Ultra Violete, Mass spectometer, absorbancia, among 
others). The advantages of python is to procces a great quantity of chromat

1. chroma_raname.py

2. chroma_plot1.py

3. merge_chanmels.py *
    This function is ready and can be called in other scripts. The idea is to use 
    for multiple folders. In my case each folder is a different experiment.

4. chroma_corrector.py

5. peak_integration.py

6. plot function.
    
