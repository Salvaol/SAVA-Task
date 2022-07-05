import pytest
import ETL.load as L
import pandas as pd
import os
import json


def test_load_csv_OK():
    assert L is not None

    csv = None
    df_created = pd.DataFrame

    df = pd.DataFrame({"time": [1, 2, 3, 4, 5], "voltage": [0.1, 0.2, 0.3, 0.4, 0.5]})
    wd = os.path.dirname(os.path.dirname(__file__))
    location = os.path.join(wd, "tests", "tests_results", "test")
    L.Load(location=location, filename="test").create_csv(dataframe=df)
    for file in os.listdir(location):
        if file.endswith(".csv"):
            csv = file
    if csv:
        df_created = pd.read_csv(os.path.join(location, csv))  # or pd.read_excel(filename) for xls file

    os.remove(os.path.join(location, csv))

    assert csv is not None
    assert not df_created.empty


def test_load_png_OK():
    assert L is not None

    png = None

    df = pd.DataFrame({"time": [1, 2, 3, 4, 5], "voltage": [0.1, 0.2, 0.3, 0.4, 0.5]})
    wd = os.path.dirname(os.path.dirname(__file__))
    location = os.path.join(wd, "tests", "tests_results", "test")
    L.Load(location=location, filename="test").create_png_from_dataframe(dataframe=df)
    for file in os.listdir(location):
        if file.endswith(".png"):
            png = file

    os.remove(os.path.join(location, png))

    assert png is not None


def test_load_json_OK():
    assert L is not None

    json_file = None
    json_created = dict()

    data = {"test": "test"}
    wd = os.path.dirname(os.path.dirname(__file__))
    location = os.path.join(wd, "tests", "tests_results", "test")
    L.Load(location=location, filename="test").create_json(data=data)
    for file in os.listdir(location):
        if file.endswith(".json"):
            json_file = file

    if json_file:
        with open(os.path.join(location, json_file)) as stream:
            json_created = json.load(stream)

    os.remove(os.path.join(location, json_file))

    assert json_file is not None
    assert json_created == {"test": "test"}


