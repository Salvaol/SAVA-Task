import numpy as np
import datetime
import pandas as pd
import math


class OCP:

    def __init__(self, time, voltage,
                 filename=None, measurement_title=None):
        """ Time in seconds, voltage in mV """

        self.time = np.array(time)
        self.voltage = np.array(voltage)

        # sampling time is in seconds
        self.sampling_time = int(self.time[1] - self.time[0])

        self.filename = filename
        self.measurement_title = measurement_title

    def experiment_duration(self):
        """ Return the experiment duration in hours """

        return math.floor(self.time[-1] / 3600)

    def discard_portions(self, discard_at_start_in_hours, discard_at_end_in_hours):
        """ 
        Discards portions at the start and at the end of the experiment
        to remove bad data due to artifacts.
        
        Portions length are expressed in hours.
        
        Returns a new OCP object.
        """

        start = math.ceil(discard_at_start_in_hours * 3600 / self.sampling_time)
        end = math.floor((self.time[-1] - (discard_at_end_in_hours * 3600)) / self.sampling_time)

        return OCP(self.time[start:end], self.voltage[start:end])

    def to_df(self, columns=None):
        """ Converts to dataframe containing time and voltage data """

        if columns is None:
            columns = ["time", "voltage"]

        return pd.DataFrame({columns[0]: self.time, columns[1]: self.voltage})

    def calculate_drift(self,
                        start_interval_duration_in_h=1,
                        end_interval_duration_in_h=1
                        ):
        """
        Calculates relevant metrics from the experiment
        
        - average potential of the first and the last interval
        - drift as difference in mV between the two average values
        - drift as % variation between the two average values
        - duration of the experiment
        
        The length of the first and last interval are expressed in hours
        and are defined by optional parameters
        start_interval_duration_in_h (default is 1h)
        end_interval_duration_in_h (default is 1h)
        """

        # sampling time in hours
        ts_in_h = self.sampling_time / 60 / 60

        # experiment duration
        duration_in_hours = self.experiment_duration()

        # selects two portions
        first_portion_end = int(start_interval_duration_in_h / ts_in_h)
        second_portion_start = int(end_interval_duration_in_h / ts_in_h)
        first_portion = self.voltage[0:first_portion_end]
        second_portion = self.voltage[-second_portion_start:]

        # average values from the two portions
        first_portion_avg = np.nanmean(first_portion)
        second_portion_avg = np.nanmean(second_portion)

        # calculate drift
        mV_diff = second_portion_avg - first_portion_avg  # in mV
        pct_diff = mV_diff / first_portion_avg * 100  # in %

        # store in dictionary
        drift_results = {
            'first_portion_avg': first_portion_avg,
            'second_portion_avg': second_portion_avg,
            'mV_diff': mV_diff, 'pct_diff': pct_diff,
            'duration_in_hours': duration_in_hours
        }

        return drift_results
