from log.log_console import logger
import sys

import ETL.functions as f
from matplotlib import pyplot as plt
import json
import os


class Load:

    def __init__(self, location, filename):
        """
        This is the general transformation class. It will contain all the required transformations.
        """
        self.location = location
        self.filename = filename

    def create_csv(self, dataframe, sep='\t', header=True):
        """
        Creates a csv in the selected path. In the future this function would upload the file instead
        :param location: String
        :param filename: String
        :param dataframe: Dataframe
        :param sep: String (Optional)
        :param header: String (Optional)
        :return:
        """
        try:
            f.create_dir(self.location)
            path = os.path.join(self.location, f"{self.filename}.csv")
            dataframe.to_csv(path_or_buf=path, sep=sep, header=header)
            logger.debug("Csv created")
        except:
            logger.error("Could not create the csv. Please check that the results folder already exists")
            sys.exit(1)

    def create_png_from_dataframe(self, dataframe, x_axis="time", x_label="Time [s]"
                                  , y_axis="voltage", y_label="Voltage [V]"):
        """Creates a png in the selected path. In the future this function would upload the file instead"""
        try:
            f.create_dir(self.location)
            path = os.path.join(self.location, f"{self.filename}.png")
            fig, ax = plt.subplots(1, 1, figsize=[12, 8])
            ax.plot(dataframe[x_axis], dataframe[y_axis])
            ax.set_ylabel(y_label)
            ax.set_xlabel(x_label)
            plt.savefig(path, bbox_inches='tight')
            logger.debug("Png created")
        except:
            logger.error("Could not create the png. Please check that the results folder already exists")
            sys.exit(1)

    def create_json(self, data):
        try:
            f.create_dir(self.location)
            path = os.path.join(self.location, f"{self.filename}.json")
            with open(path, 'w') as file:
                json.dump(data, file, indent=2)
            logger.debug("Json created")
        except:
            logger.error("Could not create the json file. Please check that the results folder already exists")
            sys.exit(1)
