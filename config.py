from aqt import mw

config = mw.addonManager.getConfig(__name__)

def current_profile_name():
    return mw.pm.name

def get_value(key):
    try:
        return config[current_profile_name()][key]
    except KeyError:
        return None

def set_value(key, value):
    if config.get(current_profile_name(), None) is not None: 
        config[current_profile_name()][key] = value
    else:
        config[current_profile_name()] = {key : value}

    mw.addonManager.writeConfig(__name__, config)