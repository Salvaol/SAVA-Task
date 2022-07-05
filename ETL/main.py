import sys
import os
import ETL.extract as E
import ETL.transform as T
import ETL.load as L
from log.log_console import logger

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
    else:
        filenames = list()
        wd = os.path.dirname(os.path.dirname(__file__))
        count = 1
        container = sys.argv[1]
        batch = sys.argv[2]
        if sys.argv[3] == "*":
            for file in os.listdir(os.path.join(wd, container, batch)):
                if file.endswith(".pssession"):
                    filenames.append(file)
        else:
            filenames = [sys.argv[3]]
        title = sys.argv[4]

        for filename in filenames:
            logger.debug(f"Processing file {count} of {len(filenames)}")
            measurements, curves = E.Extraction(container, batch, filename).extract_psfile()
            final_metrics, voltage_time = T.Transformation(curves, title).transform_pssession_files()
            location = os.path.join(wd, "results", filename.split('.')[0])
            L.Load(location=location, filename=filename.split('.')[0]).create_csv(dataframe=voltage_time)
            L.Load(location=location, filename=filename.split('.')[0]).create_json(data=final_metrics)
            L.Load(location=location, filename=filename.split('.')[0]).create_png_from_dataframe(dataframe=voltage_time)
            logger.debug(f"ETL #{count} finished")
            count += 1

