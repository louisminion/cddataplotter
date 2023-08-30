# cddataplotter
Automatically parses Applied Photophysics Circular Dichroism Spectrometer ouput and plots data in origin.
Input csv files on the command line and watch as the program creates beautiful origin plots of CD, Absorbance and g<sub>abs</sub>

Usage:
```console
user@pc:~$ python origin_conversion.py $filename
CD ORIGIN PLOTTER
 Parses Applied Photophysics Chirascan output and plots key properties in an origin project.
 Louis Minion 2023
Will process file:$filename
```
Requirements:
Requires python, numpy, pandas, originpro and a working installation of OriginLab >= 2020

Installation instructions:
- Ensure you have both Python 3.8+ and OriginLab 2020.0 or a more recent version installed.
- Install the required python libraries by running `pip -r requirements.txt`
- You're ready to go!

Known issues: 
- When working with data from older versions of Chirascan spectrometers the number of introductory lines may differ. This code has been tested on the Fuchter group Chirascan V100 output only.
