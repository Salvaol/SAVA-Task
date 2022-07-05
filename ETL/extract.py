import os
import sys

from ETL.SAVA.pspython import pspyfiles as ps
from log.log_console import logger


class Extraction:

    def __init__(self, container, batch, filename, path=None):
        """
        This is the general class for extraction. This class would contain all the connection and extractions for each
        kind of file.
        :param container: String
        :param batch: String
        :param filename: String
        :param path: String (optional)
        """
        self.container = container
        self.batch = batch
        self.filename = filename
        self.path = os.path.dirname(os.path.dirname(__file__)) if path is None else path

    def extract_psfile(self):
        """
        This function ingest a file returning the measurements and curves.
        """

        # Setting working directory
        # set path to file
        try:
            path_to_file = os.path.join(self.path, self.container, self.batch, self.filename)
            logger.debug(f"Ingesting following file:{path_to_file}")

            # Reads measurements and curves from .pssession file

            psmeasurements_with_curves = ps.load_session_file(path_to_file,
                                                              load_peak_data=False,
                                                              load_eis_fits=False,
                                                              smooth_level=0)
            if psmeasurements_with_curves == 0 or None in psmeasurements_with_curves.keys():
                logger.error("Could not find the file or pspyfiles is not well configured")
                sys.exit(1)

            # get measurement and curves
            measurement = list(psmeasurements_with_curves.keys())[0]
            curves = list(psmeasurements_with_curves.values())[0]
            logger.debug("Extraction finished")

            return measurement, curves
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)
