from datetime import date
from textwrap import dedent

from aqt import gui_hooks, mw
from PyQt5.QtWidgets import QMessageBox

from .config import get_value, set_value

will_ignore_next_sync = True

def register_to_hooks():
    gui_hooks.media_sync_did_start_or_stop.append(on_media_sync_did_start_or_stop)
    gui_hooks.profile_did_open.append(ignore_next_sync)

def on_media_sync_did_start_or_stop(running):
    if not running:
        return
    
    global will_ignore_next_sync
    if will_ignore_next_sync:
        will_ignore_next_sync = False
        return

    if get_value('last_sync_upload_date') == str(date.today()):
        return

    reply = QMessageBox.question(mw, 'Reset Ease',
        dedent('''
            WARNING: 
            Do NOT select "Yes", if you have unsynchronized data on another device or on AnkiWeb.

            Do you want to force an upload?
            The ease factor changes will not be synchronized otherwise.
        ''').strip(), 
        QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No
    )

    if reply != QMessageBox.Yes:
        return

    force_upload_on_next_sync()
    ignore_next_sync()
    set_value('last_sync_upload_date', str(date.today()))

def ignore_next_sync():
    global will_ignore_next_sync
    will_ignore_next_sync = True

def force_upload_on_next_sync():
    mw.col.scm += 1
