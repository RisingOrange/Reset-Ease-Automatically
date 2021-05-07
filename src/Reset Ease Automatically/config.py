from aqt import mw


def get(key):
    config = mw.addonManager.getConfig(__name__)
    try:
        return config[_current_profile_name()][key]
    except KeyError:
        return None


def set(key, value):
    config = mw.addonManager.getConfig(__name__)
    if config.get(_current_profile_name(), None) is not None:
        config[_current_profile_name()][key] = value
    else:
        config[_current_profile_name()] = {key: value}

    mw.addonManager.writeConfig(__name__, config)


def _current_profile_name():
    return mw.pm.name
