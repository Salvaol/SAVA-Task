import logging

# Logging attributes to show in console the API´s Log

# create logger
logger = logging.getLogger('SAVA - ETL')
logger.setLevel("DEBUG")

# create console handler and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)