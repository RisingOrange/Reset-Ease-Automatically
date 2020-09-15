from anki.lang import _
from aqt import mw

from .table_dialog import TableDialog


class PreferencesDialog(TableDialog):
    
    def __init__(self, *args, **dargs):
        super().__init__(*args, **dargs)


def show():
    mw.re_pref = PreferencesDialog(mw.app.activeWindow())
    mw.re_pref.show()
