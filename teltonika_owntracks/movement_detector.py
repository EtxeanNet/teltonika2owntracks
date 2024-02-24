from geopy import Point, distance
from typing import Callable
import logging

from teltonika_owntracks.time_deque import TimeDeque
from teltonika_owntracks.point_calculations import average

logger = logging.getLogger(__name__)

class MovementDetector:
    
    def __init__(self, averaging_seconds: float = 120, get_current_time: Callable[[], float] = TimeDeque.default_get_current_time):
        self._averaging_seconds = averaging_seconds
        self._time_deque = TimeDeque(averaging_seconds, get_current_time)

    def has_moved(self, timestamp: float, latitude: float, longitude: float, movement_limit: float = 50) -> bool:
        '''Returns true if the (latidude, longitude) has moved more than the movement_limit'''
        point = Point(latitude, longitude)
        last_points = self._time_deque.list()
        if len(last_points) > 0:
            center = average(last_points)
            self._time_deque.append(point, timestamp)
            movement = distance.distance(center, point).meters
            has_moved = movement > movement_limit
            logger.debug(f"{movement = }: { has_moved = }")
            return has_moved 
        else:
            self._time_deque.append(point, timestamp)
            return False

