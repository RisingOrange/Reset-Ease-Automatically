from aqt import mw

config = mw.addonManager.getConfig(__name__)

def get_preference(key):
    return config[key]

def set_preference(key, value):
    config[key] = value
    mw.addonManager.writeConfig(__name__, config)
