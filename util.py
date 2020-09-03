import os
from datetime import datetime, date

addon_path = os.path.dirname(__file__)
last_run_date_file = os.path.join(addon_path, 'last_run_date.txt')

def today_is_not_last_run_date():
    return date.today() != last_run_date()

def last_run_date():
    if os.path.exists(last_run_date_file):
        with open(last_run_date_file, 'r') as f:
            return datetime.strptime(f.read(), '%Y-%m-%d').date()
    else:
        return None

def set_last_run_date_to_today():
    with open(last_run_date_file, 'w') as f:
        f.write(str(date.today()))