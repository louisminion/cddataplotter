# Louis Minion 2024
# Input; csv file with two columns, wavelength and CD
# Output; csv file with two columns, wavelength and CB
# WARNING; No background subtraction done here, input already subtracted CD data
import pandas as pd
import numpy as np
import argparse
import sys
parser = argparse.ArgumentParser(
                    prog='ORDcalc',
                    description='Outputs ORD data from CD using Kramers-Kronig transformation',
                    epilog='Louis Minion 2024')
parser.add_argument('input_file')
args = parser.parse_args()
input_file = args.input_file

def Ota_Ishida(arrmu, arrCD, wvORD):
    '''
    Uses the numerical method from 
    Koji Ohta and Hatsuo Ishida, "Comparison Among Several Numerical Integration Methods for Kramers-Kronig Transformation," Appl. Spectrosc. 42, 952-957 (1988)
    as adapted in 
    Prasad L. Polavarapu,The Journal of Physical Chemistry A 2005 109 (32), 7013-7023
    '''
    j = arrmu[0]%2
    r = wvORD%2
    h = arrmu[1]-arrmu[0]
    if r == 1:
        #Assumes that data is 1nm spaced
        if j==1:
            arrmu = arrmu[1::2]
            arrCD = arrCD[1::2]
        elif j==0:
            arrmu = arrmu[0::2]
            arrCD = arrCD[0::2]
    elif r==0:
        if j==1:
            arrmu = arrmu[0::2]
            arrCD = arrCD[0::2]
        elif j==0:
            arrmu = arrmu[1::2]
            arrCD = arrCD[1::2]
    prefactor = (2/np.pi)*(2*h)*(1/2)
    Sigma = 0
    for i, mu in enumerate(arrmu):
        m = ((arrCD[i]/(wvORD-mu)) - (arrCD[i]/(wvORD+mu)))
        Sigma += m
    return prefactor*Sigma

print('#################-ORDcalc-#################')
print('Input; csv file with two columns, wavelength and CD, no column labels')
print('Output; csv file with two columns, wavelength and CB')
print('WARNING; No background subtraction done here, input already subtracted CD data')
print('\n')
print(f'Loading filename {input_file}', end='')
try:
    print('.', end='')
    df = pd.read_csv(input_file,header=None,sep=',')
    print('.', end='')
    df.columns = ['Wavelength', 'CD']
    print('.', end='')
except:
    print('Error loading input. Check format.')
    sys.exit()


print('Done', end='\n')
print('Calculating ORD using Kramers Kronig transformation.')
ORD = []
for i in df['Wavelength']:
    a = Ota_Ishida(np.array(df['Wavelength']), np.array(df['CD']), i)
    ORD.append(a)
print('Calculation completed via Ohta-Ishida method.')
print('Cite the following; Ohta and Ishida, Appl. Spectrosc. 42, 952-957 (1988), Polavarapu, J. Phys. Chem. A,(2005) 109 (32),7013-7023')
print('Saving data')
ORD = np.array(ORD)
df2 = pd.DataFrame()
df2['Wavelength'] = df['Wavelength']
df2['ORD'] = ORD
print('Exported data units are equivalent of those inputted via CD data (mdeg to mdeg etc.)')
basename = input_file[:-4]
savename = basename + 'ORD' +'.csv'
df2.to_csv(savename, index=None)
print(f'Saved as {savename}')
print('Louis Minion 2024')