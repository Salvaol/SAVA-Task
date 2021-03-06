import pytest
import ETL.extract as E
import os


def test_extract_psfile_ok_without_path():
    assert E is not None

    measurements, curves = E.Extraction('data', 'batch1', 'tc2026.pssession').extract_psfile()

    assert measurements is not None
    assert curves is not None
    assert isinstance(curves, list)


def test_extract_psfile_ok_with_path():
    assert E is not None

    measurements, curves = E.Extraction(path=os.path.dirname(os.path.dirname(__file__)), container='data'
                                        , batch='batch1', filename='tc2025.pssession').extract_psfile()

    assert measurements is not None
    assert curves is not None
    assert isinstance(curves, list)
