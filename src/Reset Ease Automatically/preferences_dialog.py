from textwrap import dedent

from anki.lang import _
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

from .config import get, set
from .table_dialog import TableDialog
from .utils import prepare_deck_to_ease_range


class PreferencesDialog(TableDialog):
    def __init__(self, *args, **dargs):
        self.window_title = "Reset Ease - Preferences"
        self.description = dedent(
            """
            For each deck listed, the Ease Factor will be reset to the specified range when Anki starts / the user profile is loaded.
            Put the same value in Ease Min and Ease Max to reset the ease factors to this value.
            All ease factors lower than Ease Min will be set to Ease Min.
            All ease factors higher than Ease Max will be set to Ease Max.
            """
        ).strip()
        self.col_names = ["Deck", "Ease Min", "Ease Max"]

        super().__init__(*args, **dargs)

    def _rows_at_start(self):
        prepare_deck_to_ease_range()
        if not get("deck_to_ease_range"):
            return []
        else:
            return [
                [deck_id, ease_range[0], ease_range[1]]
                for deck_id, ease_range in get("deck_to_ease_range").items()
            ]

    def _default_row(self):
        return [
            int(mw.col.decks.all_ids()[0]),
            250,
            250,
        ]

    def _save_preferences(self, rows):
        deck_to_ease_range = {
            row_data[0]: (row_data[1], row_data[2]) for row_data in rows
        }

        if not self._valid_ease_ranges(deck_to_ease_range):
            showInfo(
                dedent(
                    """
            The settings are invalid. 
            Please make sure that no Ease Min is bigger than the corresponding Ease Max and both are greater than zero.
            """
                ).strip()
            )
            return

        set("deck_to_ease_range", deck_to_ease_range)
        self.close()

    def _valid_ease_ranges(self, deck_to_ease):
        return all(
            0 < ease_min <= ease_max for ease_min, ease_max in deck_to_ease.values()
        )

    def _data_row_to_gui_row(self, data_row):
        def prepare_deck_combo_box():
            result = QComboBox()

            deck_names = mw.col.decks.all_names()
            result.addItems(deck_names)

            name_of_selected_deck = mw.col.decks.name(data_row[0])
            result.setCurrentText(name_of_selected_deck)
            return result

        return [
            prepare_deck_combo_box(),
            QLineEdit(str(data_row[1])),
            QLineEdit(str(data_row[2])),
        ]

    def _gui_row_to_data_row(self, gui_row):
        return [
            mw.col.decks.id(gui_row[0].currentText(), create=False),
            int(gui_row[1].text()),
            int(gui_row[2].text()),
        ]


def show():
    mw.re_pref = PreferencesDialog(mw.app.activeWindow())
    mw.re_pref.show()
