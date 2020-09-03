from datetime import datetime, date
from aqt import mw

from .preferences import get_preference, set_preference

def today_is_not_last_run_date():
    return date.today() != last_run_date()

def last_run_date():
    if get_preference("last_run_date") is None:
        return None
    return datetime.strptime(get_preference("last_run_date"), '%Y-%m-%d').date()

def set_last_run_date_to_today():
    set_preference("last_run_date", str(date.today()))