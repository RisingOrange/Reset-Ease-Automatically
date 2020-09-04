from aqt import mw
from PyQt5.QtWidgets import *

from . import preferences_dialog, ease_reset

def main():
    setup_menu()
    ease_reset.register()

def setup_menu():
    # Add "reset ease" submenu
    reset_ease_menu = QMenu("my reset ease", mw)
    mw.form.menuTools.addMenu(reset_ease_menu)

    # Add Preferences action
    a = QAction('&Preferences', mw)
    a.triggered.connect(preferences_dialog.show)
    reset_ease_menu.addAction(a)

main()
