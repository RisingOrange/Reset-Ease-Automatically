from textwrap import dedent

from anki.lang import _
from aqt import mw
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .config import get_value, set_value
from .table_dialog import TableDialog
from .utils import clean_up_deck_to_ease


class PreferencesDialog(TableDialog):
    
    def __init__(self, *args, **dargs):
        self.window_title = 'Reset Ease - Preferences'
        self.description = dedent('''
            For each deck listed, the Ease Factor will be reset to the specified value when Anki starts / the user profile is loaded.
            '''
        ).strip()
        self.col_names = ['Deck', 'Ease']

        super().__init__(*args, **dargs)


    def _rows_at_start(self):
        clean_up_deck_to_ease()
        if not get_value('deck_to_ease'):
            return []
        else:
            return list(get_value('deck_to_ease').items())

    def _save_preferences(self):
        deck_to_ease = {
            row_data[0] : row_data[1]
            for row_data in self._rows()
        }

        set_value('deck_to_ease', deck_to_ease)
        self.close()

    def _default_row(self):
        return [
            int(mw.col.decks.allIds()[0]), 
            250,
        ]


    def _data_row_to_gui_row(self, data_row):

        def prepare_deck_combo_box():
            result = QComboBox()

            deck_names = mw.col.decks.allNames()
            result.addItems(deck_names)

            name_of_selected_deck = mw.col.decks.name(data_row[0])
            result.setCurrentText(name_of_selected_deck)
            return result

        return [
            prepare_deck_combo_box(),
            QLineEdit(str(data_row[1]))
        ]

    def _gui_row_to_data_row(self, gui_row):
        return [
            mw.col.decks.id(gui_row[0].currentText(), create=False),
            int(gui_row[1].text()),
        ]


def show():
    mw.re_pref = PreferencesDialog(mw.app.activeWindow())
    mw.re_pref.show()
