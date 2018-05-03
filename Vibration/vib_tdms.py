import pandas as pd
from nptdms import tdms

tdmspath = './TDMS/vib.tdms'
tdfile = tdms.TdmsFile(tdmspath)
data = tdfile.channel_data('Vibration', 'DOC X')
dataProp = tdfile.group_channels('Vibration')[0].properties

print(dataProp)

DOCSensitivity = float(dataProp['Sensor Sensitivity (mV/EU)'])
y = data / (DOCSensitivity / 1000)
fs = 8533.33333333

win_size = 2**13
fft_size = win_size

print('y shape:', y.shape)

def printStats():
    print('hi')


if __name__ == '__main__':
    printStats()
