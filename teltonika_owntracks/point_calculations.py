from geopy import Point
from math import radians, sin, cos, sqrt, atan2, pi

import numpy as np
import numpy.linalg as lin

E = np.array([[ 0, 0, 1],
              [ 0, 1, 0],
              [-1, 0, 0]])

def average_n_vector(points: list[Point]) -> Point:
    '''
    Calculate average point based on n-vector calculations
    
    See https://stackoverflow.com/a/68243962 and https://www.ffi.no/en/research/n-vector/#example_7
    '''
    res = []
    for point in points:
        res.append(_lat_long2n_E(point.latitude,point.longitude))
    res = np.array(res)
    m = np.mean(res,axis=0)
    m = m / lin.norm(m)
    lat, lon = _n_E2lat_long(m)
    alt = np.mean([p.altitude for p in points])
    return Point(lat, lon, alt) 

def _lat_long2n_E(latitude,longitude):
    res = [np.sin(np.deg2rad(latitude)),
           np.sin(np.deg2rad(longitude)) * np.cos(np.deg2rad(latitude)),
           -np.cos(np.deg2rad(longitude)) * np.cos(np.deg2rad(latitude))]
    return np.dot(E.T,np.array(res))

def _n_E2lat_long(n_E):
    n_E = np.dot(E, n_E)
    longitude=np.arctan2(n_E[1],-n_E[2]);
    equatorial_component = np.sqrt(n_E[1]**2 + n_E[2]**2 );
    latitude=np.arctan2(n_E[0],equatorial_component);
    return np.rad2deg(latitude), np.rad2deg(longitude)
   
def average(points):
    """
    Calculate the average point from a list of geopy.Point coordinates, considering the meridians.
    
    :param points: List of geopy.Point coordinates.
    :return: geopy.Point representing the average point.
    """
    total_x = 0
    total_y = 0
    total_z = 0

    for point in points:
        lat_rad = radians(point.latitude)
        lon_rad = radians(point.longitude)

        x = cos(lat_rad) * cos(lon_rad)
        y = cos(lat_rad) * sin(lon_rad)
        z = sin(lat_rad)

        total_x += x
        total_y += y
        total_z += z

    avg_x = total_x / len(points)
    avg_y = total_y / len(points)
    avg_z = total_z / len(points)

    avg_lon_rad = atan2(avg_y, avg_x)
    avg_lat_rad = atan2(avg_z, sqrt(avg_x**2 + avg_y**2))

    avg_lat = degrees(avg_lat_rad)
    avg_lon = degrees(avg_lon_rad)

    return Point(latitude=avg_lat, longitude=avg_lon)

def degrees(radians):
    """
    Convert radians to degrees.
    """
    return radians * 180 / pi