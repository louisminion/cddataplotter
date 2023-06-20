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
Requires numpy, pandas, originpro and a working installation of OriginLab >= 2020
