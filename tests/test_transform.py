import pytest
import ETL.extract as E
from ETL.SAVA.ocp_data import OCP
import pandas as pd
import ETL.functions as f
import ETL.transform as T


def test_OCP_duration_in_hours_OK():
    assert E is not None
    assert OCP is not None

    measurements, curves = E.Extraction(container='data'
                                        , batch='batch1', filename='tc2025.pssession').extract_psfile()
    index = f.get_curve_position(curves, "OCP E vs t")
    time = curves[index].x_array
    voltage = curves[index].y_array
    hours = OCP(time=time, voltage=voltage).experiment_duration()

    assert hours is not None
    assert isinstance(hours, int)
    assert hours == 55


def test_OCP_remove_bad_data_OK():
    assert E is not None
    assert OCP is not None

    measurements, curves = E.Extraction(container='data'
                                        , batch='batch1', filename='tc2025.pssession').extract_psfile()
    index = f.get_curve_position(curves, "OCP E vs t")
    time = curves[index].x_array
    voltage = curves[index].y_array
    new_curve = OCP(time=time, voltage=voltage).discard_portions(1, 2)

    assert new_curve is not None
    assert isinstance(new_curve, OCP)
    assert new_curve.time[0] >= 3600
    assert new_curve.time[-1] <= curves[index].x_array[-1] - (2 * 3600)


def test_OCP_to_df_OK():
    assert E is not None
    assert OCP is not None

    measurements, curves = E.Extraction(container='data'
                                        , batch='batch1', filename='tc2025.pssession').extract_psfile()
    index = f.get_curve_position(curves, "OCP E vs t")
    time = curves[index].x_array
    voltage = curves[index].y_array
    ocp_df = OCP(time=time, voltage=voltage).to_df()

    assert ocp_df is not None
    assert isinstance(ocp_df, pd.DataFrame)
    assert ocp_df.columns[0] == "time"
    assert ocp_df.columns[1] == "voltage"
    assert ocp_df.values is not None
    assert len(ocp_df.values) >= 1


def test_transform_pssession_files_OK():
    assert E is not None
    assert OCP is not None

    measurements, curves = E.Extraction(container='data'
                                        , batch='batch1', filename='tc2025.pssession').extract_psfile()
    drift, df = T.Transformation(curves, "OCP E vs t").transform_pssession_files()

    assert drift is not None
    assert isinstance(drift, dict)
    assert isinstance(df, pd.DataFrame)
    assert df.columns[0] == "time"
    assert df.columns[1] == "voltage"
    assert df.values is not None
    assert len(df.values) >= 1
