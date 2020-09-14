import importlib

from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo
from PyQt5.QtWidgets import *

from . import preferences_dialog
from .reset_ease import reset_ease
from .store_restore_ease import add_deck_options


def main():
    setup_toolbar_menu()

    try:
        gui_hooks = importlib.import_module('aqt.gui_hooks')
    except Exception:
        pass # older version of Anki do not have this hook, in this case do nothing
    else:
        gui_hooks.media_sync_did_start_or_stop.append(lambda running: reset_ease() if not running else None)
    
    addHook('unloadProfile', reset_ease)

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
    a.triggered.connect(on_reset_ease_button_clicked)
    reset_ease_menu.addAction(a)

def on_reset_ease_button_clicked():
    reset_ease()
    showInfo(title="Reset Ease", text="Done")

main()
