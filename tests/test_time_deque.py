from datetime import datetime, timedelta
import time

from teltonika_owntracks.time_deque import TimeDeque


def test_time_deque():
    now = datetime.now()
    td = TimeDeque(180)
    td.append('a', datetime.timestamp(now - timedelta(seconds=210)))
    td.append('b', datetime.timestamp(now - timedelta(seconds=150)))
    td.append('c', datetime.timestamp(now - timedelta(seconds=50)))
    td.append('d', datetime.timestamp(now))

    assert len(td) == 3
    assert td.list() == ['b', 'c', 'd']

def test_default_get_current_time():
    now = datetime.timestamp(datetime.now())
    td = TimeDeque(180)
    time.sleep(1)
    ts = td._get_current_time()
    assert ts > now


    
    
    