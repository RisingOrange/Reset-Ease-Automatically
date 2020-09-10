from aqt import gui_hooks, mw
from aqt.utils import showInfo
from PyQt5.QtWidgets import *

from . import preferences_dialog
from .reset_ease import add_deck_options, reset_ease


def main():
    setup_toolbar_menu()

    gui_hooks.media_sync_did_start_or_stop.append(lambda running: reset_ease() if not running else None)
    gui_hooks.profile_will_close.append(reset_ease)
    
    gui_hooks.deck_browser_will_show_options_menu.append(add_deck_options)
    
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
