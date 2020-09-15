from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo, tooltip
from PyQt5.QtWidgets import *

from . import preferences_dialog
from .reset_ease import reset_ease
from .store_restore_ease import add_deck_options

import importlib


def main():
    setup_toolbar_menu()
    
    addHook('unloadProfile', reset_ease_and_show_message)

    try:
        gui_hooks = importlib.import_module('aqt.gui_hooks')
        gui_hooks.sync_did_finish.append(reset_ease_and_show_message)
    except Exception:
        pass # Older anki versions do not have this module / hook, in this case do nothing        

    addHook('showDeckOptions', add_deck_options)
    
    mw.addonManager.setConfigAction(__name__, preferences_dialog.show)

def setup_toolbar_menu():
    # Add "reset ease" submenu
    reset_ease_menu = QMenu("Reset Ease", mw)
    mw.form.menuTools.addMenu(reset_ease_menu)

    # Add Preferences button
    a = QAction('&Preferences', mw)
    a.triggered.connect(preferences_dialog.show)
    reset_ease_menu.addAction(a)

    # Reset Ease button
    a = QAction('&Reset Ease', mw)
    a.triggered.connect(reset_ease_and_show_message)
    reset_ease_menu.addAction(a)

def reset_ease_and_show_message():
    reset_ease()
    tooltip("Ease factors have been reset", period=1200)

main()
