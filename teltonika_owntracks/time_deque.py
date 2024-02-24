import collections
from dataclasses import dataclass
import typing
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class DequeItem:
    time: float
    value: typing.Any

class TimeDeque:
    """
    A timedeque is a deque which will keep records for the specified time period
    """

    @staticmethod
    def default_get_current_time() -> float:
        return datetime.timestamp(datetime.utcnow())

    def __init__(self, time_window_seconds: int = 300, get_current_time: typing.Callable[[], float] = default_get_current_time):
        self._time_window_seconds = time_window_seconds
        self._deque = collections.deque()
        self._get_current_time = get_current_time
   
    def prune(self) -> bool:
        """
        Remove any items from the left of the deque which are older than
        `self.time_window_seconds`. Can probably be called less and save
        some time if we delegate use of this to the programmer.
        """

        try:
            while self._get_current_time() - self._deque[0].time > self._time_window_seconds:
                self._deque.popleft()
        except IndexError as e:
            """
            If self._deque[0] fails, the deque is empty
            """
            return True

        logger.debug("Pruned %d items from deque", len(self._deque))
        return True

    def append(self, item, time: float | None = None) -> bool:
        store_time = time or self._get_current_time()
        self._deque.append(DequeItem(store_time, item))
        assert self.prune()
        return True

    def list(self) -> list[typing.Any]:
        self.prune()
        return [it.value for it in list(self._deque)]

    def __len__(self) -> int:
        self.prune()
        return len(self._deque)

    def __iter__(self):
        self.prune()
        for ob in self._deque:
            yield ob.value