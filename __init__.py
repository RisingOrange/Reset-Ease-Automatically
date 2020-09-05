from aqt import gui_hooks, mw
from aqt.utils import showInfo
from PyQt5.QtWidgets import *

from . import preferences_dialog
from .reset_ease import reset_ease


def main():
    setup_menu()
    gui_hooks.profile_did_open.append(reset_ease)
    mw.addonManager.setConfigAction(__name__, preferences_dialog.show)

def setup_menu():
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
