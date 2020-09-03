from datetime import datetime, date
from aqt import mw

config = mw.addonManager.getConfig(__name__)

def today_is_not_last_run_date():
    return date.today() != last_run_date()

def last_run_date():
    if config["last_run_date"] is None:
        return None
    return datetime.strptime(config["last_run_date"], '%Y-%m-%d').date()

def set_last_run_date_to_today():
    config["last_run_date"] = str(date.today())
    mw.addonManager.writeConfig(__name__, config)