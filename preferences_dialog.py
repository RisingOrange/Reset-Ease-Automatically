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
        self.col_names = ['Deck', 'Ease']

        super().__init__(*args, **dargs)


    def _rows_at_start(self):
        clean_up_deck_to_ease()
        if not get_value('deck_to_ease'):
            return []
        else:
            return [
                {
                    'Deck' : deck_id, 
                    'Ease' : ease,
                }
                for deck_id, ease in get_value('deck_to_ease').items()
            ]

    def _save_preferences(self):
        deck_to_ease = {
            row_data['Deck'] : row_data['Ease']
            for row_data in self._rows()
        }

        set_value('deck_to_ease', deck_to_ease)
        self.close()

    def _default_row(self):
        return {
            'Deck' : int(mw.col.decks.allIds()[0]), 
            'Ease' : 250,
        }

    def _data_row_to_gui_row(self, data_row):

        def prepare_deck_combo_box():
            result = QComboBox()

            deck_names = mw.col.decks.allNames()
            result.addItems(deck_names)

            name_of_selected_deck = mw.col.decks.name(data_row['Deck'])
            result.setCurrentText(name_of_selected_deck)
            return result

        result = {}
        result['Deck'] = prepare_deck_combo_box()
        result['Ease'] = QLineEdit(str(data_row['Ease']))
        return result

    def _gui_row_to_data_row(self, gui_row):
        result = {}
        result['Deck'] = mw.col.decks.id(gui_row[0].currentText(), create=False)
        result['Ease'] = int(gui_row[1].text())
        return result


def show():
    mw.re_pref = PreferencesDialog(mw.app.activeWindow())
    mw.re_pref.show()
