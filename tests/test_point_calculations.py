from teltonika_owntracks.point_calculations import average_n_vector, average
from geopy import Point
import pytest

def test_average():
    libya = Point(30,20)
    france = Point(47,3)
    points = [libya, france]
    middle = average_n_vector(points)
    middle2 = average(points)

    assert middle.latitude == pytest.approx(middle2.latitude,  0.0000001)
    assert middle.longitude == pytest.approx(middle2.longitude,0.0000001)


def test_average_close_to_180():
    west = Point(30,-179)
    east = Point(30,179)
    points = [west, east]
    middle = average_n_vector(points)
    middle2 = average(points)

    assert middle.latitude == pytest.approx(middle2.latitude,  0.0000001)
    assert middle.longitude == pytest.approx(middle2.longitude,0.0000001)
    assert middle.longitude == 180

