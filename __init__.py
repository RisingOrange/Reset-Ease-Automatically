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

    # Reset Ease and Force Upload on next Sync
    a = QAction('&Reset Ease and Force Upload on next Sync', mw)
    a.triggered.connect(lambda : ease_reset.reset_ease_of_selected_decks_and_force_sync(show_message=True))
    reset_ease_menu.addAction(a)

    # Add Preferences action
    a = QAction('&Preferences', mw)
    a.triggered.connect(preferences_dialog.show)
    reset_ease_menu.addAction(a)

main()
