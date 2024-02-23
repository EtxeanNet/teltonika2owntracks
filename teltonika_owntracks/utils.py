from datetime import datetime
import calendar

def to_timestamp(dt: datetime):
    return calendar.timegm(dt.timetuple())