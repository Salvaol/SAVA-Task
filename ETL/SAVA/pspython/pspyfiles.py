import clr
import os
import sys
from ETL.SAVA.pspython import pspydata as pspydata
import pandas as pd

# Load DLLs
scriptDir = os.path.dirname(os.path.realpath(__file__))

# This dll contains the classes in which the data is stored
clr.AddReference(os.path.join(scriptDir, 'PalmSensNew.Core.dll'))

# This dll is used to load your session file
clr.AddReference(os.path.join(scriptDir, 'PalmSensNew.Core.Windows.dll'))


# Import the static LoadSaveHelperFunctions
from PalmSens.Windows import LoadSaveHelperFunctions


def load_session_file(path, **kwargs):
    load_peak_data = kwargs.get('load_peak_data', False)
    load_eis_fits = kwargs.get('load_eis_fits', False)
    smooth_level = kwargs.get('smooth_level', 0)

    try:
        session = LoadSaveHelperFunctions.LoadSessionFile(path)
        
        measurements_with_curves = {}
        for m in session:

            try:
                curves_ = pspydata.convert_to_curves(m)
            except Exception as e:

                curves_ = None
            
            try:
                meas_ = pspydata.convert_to_measurement(m, load_peak_data=load_peak_data, load_eis_fits=load_eis_fits, smooth_level=smooth_level)
            except:
                print('Could not read measurements from this file:')
                print(path)
                print('Measurement:')
                print(m.Title)
                meas_ = None
                
            measurements_with_curves[meas_] = curves_

        return measurements_with_curves
    except:
        error = sys.exc_info()[0]
        print(error)
        return 0
    
    
def load_method_file(path):
    try:
        method = LoadSaveHelperFunctions.LoadMethod(path)
        return method
    except:
        return 0


def get_method_estimated_duration(path):
    method = load_method_file(path)
    if method == 0:
        return 0
    else:
        return method.MinimumEstimatedMeasurementDuration


# %% Lorenzo


def to_df(psmeasurements_with_curves):
    """ Converts measurements with curves into dataframe """
    
    df_by_measurement = {}
    
    for measurement, curves in psmeasurements_with_curves.items():
        
        # time is common for a measurement
        time = measurement.time_arrays[0]
        
        timestamp = measurement.timestamp
        
        # check if timestamp format is good
        if 'AM' in timestamp:
            timestamp = timestamp.replace(' AM', '')
            format_ = '%m/%d/%Y %H:%M:%S'
        elif 'PM' in timestamp:
            timestamp = timestamp.replace(' PM', '')
            date, time = timestamp.split(' ')
            h, m, s = time.split(':')
            h = int(h)
            h = h + 12
            h = str(h)
            timestamp = F'{date} {h}:{m}:{s}'
            format_ = '%m/%d/%Y %H:%M:%S'
        else:
            format_='%d/%m/%Y %H:%M:%S'
        
        # real timestamps from file info
        session_start = pd.to_datetime(timestamp, format=format_)
        real_time = pd.to_timedelta(time, unit='s') + session_start
        # real_time = real_time - pd.to_timedelta(len(time), unit='s')  # I really hope this never changes again
        
        # read all the curves
        data_ = {}
        for curve in curves:
            # makes a dataframe
            df = pd.DataFrame({'x': curve.x_array, 'y': curve.y_array})
            # sets dataframe index as timedelta using x values
            df.index = pd.to_timedelta(curve.x_array, unit='s')
            
            # resamples to 1 second sampling time
            # TODO: this assumes everything is sampled with 1 second, you need to fix this :(
            df = df.resample('1s').mean()
            # curve data
            data_[curve.type] = df['y'].to_numpy()
            
        # if we trim a curve, usually it's the last portion, so the rest need to be adjusted to the same length
        min_length = min([len(data_[k]) for k in data_])
        for k in data_:
            data_[k] = data_[k][0:min_length]
        
        df = pd.DataFrame(data_)  # dictionary to dataframe
        df.loc[:, 'Time'] = time[0:min_length]
        df.loc[:, 'Real time'] = real_time[0:min_length]
        
        # store this measurement data
        df_by_measurement[measurement.Title] = df
        
    return df_by_measurement


def read_notes(path, n_chars=3000):
    """ Read ps notes to get substrate addition times """
    with open(path, 'r', encoding="utf16") as myfile:
        contents = myfile.read()
    raw_txt = contents[1:n_chars].split('\\r\\n')
    notes_txt = [x for x in raw_txt if 'NOTES=' in x]
    notes_txt = notes_txt[0].replace('%20', ' ').replace('NOTES=', '').replace('%crlf', os.linesep)
    return notes_txt