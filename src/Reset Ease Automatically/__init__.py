from anki.hooks import addHook
from aqt import gui_hooks, mw
from aqt.qt import *
from aqt.utils import tooltip

from . import preferences_dialog
from .compat import setup_compat_aliases
from .reset_ease import reset_ease
from .store_restore_ease import add_deck_options


def main():
    setup_toolbar_menu()

    addHook("unloadProfile", reset_ease_and_show_message)

    addHook("showDeckOptions", add_deck_options)

    mw.addonManager.setConfigAction(__name__, preferences_dialog.show)


def setup_toolbar_menu():
    # Add "reset ease" submenu
    reset_ease_menu = QMenu("Reset Ease", mw)
    mw.form.menuTools.addMenu(reset_ease_menu)

    # Add Preferences button
    a = QAction("&Preferences", mw)
    a.triggered.connect(preferences_dialog.show)
    reset_ease_menu.addAction(a)

    # Reset Ease button
    a = QAction("&Reset Ease", mw)
    a.triggered.connect(reset_ease_and_show_message)
    reset_ease_menu.addAction(a)


def reset_ease_and_show_message():
    reset_ease()
    tooltip("Ease factors have been reset", period=1200)


main()


gui_hooks.profile_did_open.append(setup_compat_aliases)
