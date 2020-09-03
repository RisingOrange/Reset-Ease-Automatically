import importlib

from aqt import mw
from PyQt5.QtWidgets import *

from . import main

def on_preferences_dialog():
    from . import preferences_dialog
    importlib.reload(preferences_dialog)
    preferences_dialog.main()

def main():
    # Add "reset ease" submenu
    reset_ease_menu = QMenu("my reset ease", mw)
    mw.form.menuTools.addMenu(reset_ease_menu)

    # Add menu button
    a = QAction('&Preferences', mw)
    a.triggered.connect(on_preferences_dialog)
    reset_ease_menu.addAction(a)

main()