from log.log_console import logger
import os
import sys
from ETL.SAVA.ocp_data import OCP
import ETL.functions as f


class Transformation:

    def __init__(self, curves, title):
        """
        This is the general transformation class. It will contain all the required transformations.
        """
        self.curves = curves
        self.title = title

    def transform_pssession_files(self, discard_at_start_in_hours=1, discard_at_end_in_hours=2):
        """
        This file transform the ingested files.
        :param curves: Curve
        :param title: String
        :param discard_at_start_in_hours: Int (Optional)
        :param discard_at_end_in_hours: Int (Optional)
        :return:
        """
        try:
            index = f.get_curve_position(self.curves, self.title)
            time = self.curves[index].x_array
            voltage = self.curves[index].y_array
            new_curve = OCP(time=time, voltage=voltage).discard_portions(discard_at_start_in_hours, discard_at_end_in_hours)
            final_metrics = new_curve.calculate_drift()
            voltage_time = new_curve.to_df()

            logger.debug("Transformation finished")
            return final_metrics, voltage_time

        except Exception as e:
            logger.error(str(e))
            sys.exit(1)
