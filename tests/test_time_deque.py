from datetime import datetime, timedelta

from teltonika_owntracks.time_deque import TimeDeque


def test_time_deque():
    now = datetime.utcnow()
    td = TimeDeque(180)
    td.append('a', datetime.timestamp(now - timedelta(seconds=210)))
    td.append('b', datetime.timestamp(now - timedelta(seconds=150)))
    td.append('c', datetime.timestamp(now - timedelta(seconds=50)))
    td.append('d', datetime.timestamp(now))

    assert len(td) == 3
    assert td.list() == ['b', 'c', 'd']




    
    
    