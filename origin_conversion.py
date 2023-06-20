import originpro as op
import pandas as pd
import numpy as np
import re
import argparse
import pathlib
import threading
import itertools, sys
spinner = itertools.cycle(['-', '/', '|', '\\'])
print('CD ORIGIN PLOTTER \n Parses Applied Photophysics Chirascan output and plots key properties in an origin project. \n Louis Minion 2023')

def loadCDdata(filename):
    with open(filename) as f:
        g = f.readlines()

    experimentinfo = {}
    for i in range(0,33):
        line = g[i]
        if line == '\n':
        # print('break')
            continue
        if ':' not in line:
            continue
        if 'Wavelength' in line:
            w = line
            ls = re.split(',', w)[1:]
            for j in ls:
                # print(j)
                [title, value] = re.split(':', j)
                experimentinfo[title] = value
            continue 
        try:
            [title, value] = re.split(':', line)
        except ValueError:
            continue
        experimentinfo[title] = value

    n= re.split('-', experimentinfo['Wavelength'])
    for i,N in enumerate(n):
        n[i]= float(N.strip()[:-2])
    experimentinfo['StartWavelength'] = n[1]
    experimentinfo['EndWavelength'] = n[0]
    nws = int(experimentinfo['StartWavelength']-experimentinfo['EndWavelength']+1)
    CDdf = pd.read_csv(filename, skiprows=37, nrows=nws, header=None)
    CDdf.columns =['Wavelength', 'CD']
    HVdf = pd.read_csv(filename, skiprows=(37+3+int(nws)), nrows=nws,header=None)
    HVdf.columns = ['Wavelength', 'HV']
    Absdf = pd.read_csv(filename, skiprows=(37+6+2*int(nws)), nrows=nws,header=None)
    Absdf.columns = ['Wavelength', 'Abs']
    Voltagedf = pd.read_csv(filename, skiprows=(37+9+3*int(nws)), nrows=nws,header=None)
    Voltagedf.columns = ['Wavelength', 'Voltage']
    Countdf = pd.read_csv(filename, skiprows=(37+12+4*int(nws)), nrows=nws,header=None)
    Countdf.columns = ['Wavelength', 'Count']
    SEdf = pd.read_csv(filename, skiprows=(37+15+5*int(nws)), nrows=nws,header=None)
    SEdf.columns = ['Wavelength', 'SE']
    Tempdf = pd.read_csv(filename, skiprows=(37+18+6*int(nws)), nrows=nws,header=None)
    Tempdf.columns = ['Wavelength', 'Temp']
    result = {'experimentinfo':experimentinfo, 'CD':CDdf, 'HV':HVdf, 'Abs':Absdf, 'Voltage':Voltagedf, 'Count':Countdf, 'SE':SEdf, 'Temp':Tempdf}
    return result




# Ensures that the Origin instance gets shut down properly.
import sys
def origin_shutdown_exception_hook(exctype, value, traceback):
    op.exit()
    sys.__excepthook__(exctype, value, traceback)
if op and op.oext:
    sys.excepthook = origin_shutdown_exception_hook


# Set Origin instance visibility.
if op.oext:
    op.set_show(True)

# YOUR CODE HERE
parser = argparse.ArgumentParser(
                    prog='Chirascan Origin Plotter',
                    description='Parses Applied Photophysics Chirascan output and plots key properties in an origin project.',
                    epilog='Louis Minion 2023')

parser.add_argument('filename', metavar='f', type=str,
                    help='File to be converted.')
args = parser.parse_args()
filename = args.filename
filenamepath = pathlib.Path(filename)
print('Will process file:{}'.format(filename))
def createOriginBook(filenamepath):
    filename = str(filenamepath)
    results = loadCDdata(filename)
    book = op.new_book('w')

    book.lname = 'Experimental Data:{}'.format(filenamepath.name)
    # Get 1st sheet from book.
    wks = book[0]
    # Set sheet short name.
    wks.name = 'Data'
    wks.from_list(0,results['CD']['Wavelength'], axis='X', lname='Wavelength', units='nm')
    wks.from_list(1,results['CD']['CD'], axis='Y', lname='CD', units='mdeg')
    wks.from_list(2,results['Abs']['Abs'], axis='Y', lname='Abs', units='A.U.')
    wks.from_list(3,results['HV']['HV'], axis='Y', lname='HV', units='V')
    wks.from_list(4,results['SE']['SE'], axis='Y', lname='SE', units='arb.')
    wks.from_list(5,results['Voltage']['Voltage'], axis='Y', lname='Voltage', units='V')
    wks.from_list(6,results['Count']['Count'], axis='Y', lname='Count', units='arb.')
    wks.from_list(7,results['Temp']['Temp'], axis='Y', lname='Temp', units='C')
    gfactor = results['CD']['CD']/(32982*results['Abs']['Abs'])
    wks.from_list(8,gfactor, axis='Y', lname='g')


    graph = op.new_graph()
    gl=graph[0]
    # plot whole sheet as XY plot
    plot = gl.add_plot(wks,colx=0, coly=1, type='l')
    gl.rescale()

    layr = gl
    pindex = gl.index()
    pname = layr.obj.GetStrProp(f'plot{pindex+1}.name')
    layr.lt_exec(f'set {pname} -w 2500')
    plot.color = '#ff0000'


    absg = op.new_graph()
    agl = absg[0]
    aplot = agl.add_plot(wks, colx=0, coly=2, type='l')
    agl.rescale()
    layr = agl
    pindex = agl.index()
    pname = layr.obj.GetStrProp(f'plot{pindex+1}.name')
    layr.lt_exec(f'set {pname} -w 2500')
    aplot.color = '#ff0000'
    ggr = op.new_graph()
    ggrgl = ggr[0]
    gplot = ggrgl.add_plot(wks, colx=0, coly=8, type='l')
    ggrgl.rescale()
    layr = ggrgl
    pindex = ggrgl.index()
    pname = layr.obj.GetStrProp(f'plot{pindex+1}.name')
    layr.lt_exec(f'set {pname} -w 2500')
    gplot.color = '#ff0000'
    # Save the opju.
    op.save('{}.opju'.format(str(filename)[:-4]))
    return False

t = threading.Thread(target=createOriginBook, args=[filenamepath])
t.run()
while t.is_alive():
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')     

# Exit running instance of Origin.
if op.oext:
    op.exit()