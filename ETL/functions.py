from log.log_console import logger
import sys
import os


def get_curve_position(curves, title):
    """Returns the position of a curve in an array based on the title
    :param curves: Curves
    :param title: String
    :return:
    """
    try:
        return [i for i in range(len(curves)) if curves[i].Title == title][0]

    except:
        logger.error(f"The Title '{title}' does not exists for this curves.")
        sys.exit(1)


def create_dir(location):
    if not os.path.exists(location):
        os.mkdir(location)

