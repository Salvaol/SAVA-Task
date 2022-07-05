import ETL.functions as f
import os


class Curve:
    def __init__(self, title):
        self.Title = title


def test_get_curve_position_OK():
    assert f is not None
    test_curve = Curve("test")
    correct_curve = Curve("Correct")
    curves = [test_curve, test_curve, correct_curve, test_curve]
    index = f.get_curve_position(curves, "Correct")

    assert index == 2


def test_create_dir_OK():
    assert f is not None

    wd = os.path.dirname(os.path.dirname(__file__))
    location = os.path.join(wd, "tests", "test_dir")

    assert not os.path.exists(location)

    f.create_dir(location)

    assert os.path.exists(location)

    os.rmdir(location)

