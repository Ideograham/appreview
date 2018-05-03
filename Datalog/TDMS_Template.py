import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import dtdms
import wpphist
# %matplotlib inline

class TestingDefaults(object):
    def __init__(self):
        self.perf_curve_cac_min = 48  #degrees C
        self.perf_curve_cac_max = 56  #degrees C
        self.perf_curve_max_top_tank = 113 #degrees C
        self.perf_curve_min_water_pump_inlet_95C = 110 #kPa
        self.perf_curve_max_intake_restriction = -3.75 #kPa

def getTDMSFilesToProcess(path = '.', filename = ''):
    files = sorted(list(set(os.listdir(path))))
    tdms_files = []
    for file in files:
        extension = file.split('.')[-1]
        if (extension == 'tdms'):
            # print('Processing %s' %file)
            tdms_files.append(file)
    return(tdms_files)

def processTDMS(df, td):
    #CONSTANTS
    # perf_curve_cac_min = 48  #degrees C
    # perf_curve_cac_max = 56  #degrees C
    # perf_curve_max_top_tank = 113 #degrees C
    # perf_curve_min_water_pump_inlet_95C = 110 #kPa
    # perf_curve_max_intake_restriction = -3.75 #kPa

    #Standard Calculations
    df['Ambient'] = df.tT01_Ambient_Air_01 #+ df.tT02_Ambient_Air_02) / 2.0
    df['CorrectedCAC'] = 25 - df.Ambient + df.cCACOutTemp
    df['LAT'] = td.perf_curve_max_top_tank - df.cCoolantTemp + df.Ambient
    df['IntakeTempRise'] = df.tT03_Air_Cleaner_Inlet - df.Ambient
    df['IntakeRestrictionAvailable'] = df.pP01_Intake_Air_Restriction - td.perf_curve_max_intake_restriction

    df.plot(figsize=(18,24), color=('r'), subplots=True );
    #FIGURE out how to get the range from this chart.
    #then display the rest of them using only the range.
    #could try to auto set it....based on when things stablilze.

    #ONLY USE STABLE PORTION FOR RESULTS
    test_subset = df[600:1000]
    section_plot = test_subset.plot(figsize=(18,24), color = ('g'), subplots=True);
    wpphist.plot(data=test_subset['IntakeTempRise'].values, ylabel='Count', xlabel='Temperature (degC)', 
             title='Intake Temp Rise (degC) Histogram', color='green');
    wpphist.plot(data=test_subset['IntakeRestrictionAvailable'].values, ylabel='Count', xlabel='Pressure (kPa)', 
             title='Intake Restriction Margin (kPa) Histogram', color='pink');
    wpphist.plot(data=test_subset['CorrectedCAC'].values, ylabel='Count', xlabel='Temperature (degC)', 
             title='Corrected CAC (degC) Histogram', color='blue');
    wpphist.plot(data=test_subset['LAT'].values, ylabel='Count', xlabel='Temperature (degC)', 
             title='Limiting Ambient Temperature (degC) Histogram', color='orange');

def processFiles(tdms_files, test_defaults):
    
    for file in tdms_files:
        tdms = dtdms.drivetdms(file)
        df = pd.DataFrame(tdms.data_dict)
        print('Processing file %s' %file)
        print('%s contains the following data:\n%s' %(file, df.columns.values))
        df = processTDMS(df)

def main():
    TestingDefaults td = new TestingDefaults()
    files = []
    files = getTDMSFilesToProcess(path='.\\tdms\\')
    print('wtf')
    print(files)
    processFiles(files, td)

if __name__ == "__main__":
    main()
