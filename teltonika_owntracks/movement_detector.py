from geopy import Point, distance
from typing import Callable
import logging

from teltonika_owntracks.time_deque import TimeDeque
from teltonika_owntracks.point_calculations import average

logger = logging.getLogger(__name__)

class MovementDetector:
    
    def __init__(self, history_seconds: float = 120, movement_limit: float = 50, get_current_time: Callable[[], float] = TimeDeque.default_get_current_time):
        self._time_deque = TimeDeque(history_seconds, get_current_time)
        self._movement_limit = movement_limit
        logger.info(f'Initialized MovementDetector with a history of {history_seconds} s and a movement limit of {movement_limit} m')

    def has_moved(self, timestamp: float, latitude: float, longitude: float) -> bool:
        '''Returns true if the (latidude, longitude) has moved more than the movement_limit'''
        point = Point(latitude, longitude)
        last_points = self._time_deque.list()
        if len(last_points) > 0:
            center = average(last_points)
            self._time_deque.append(point, timestamp)
            movement = round(distance.distance(center, point).meters, 2)
            has_moved = movement > self._movement_limit
            logger.debug(f"{movement = }, { self._movement_limit = }: { has_moved = }")
            return has_moved 
        else:
            self._time_deque.append(point, timestamp)
            return False

