import aqt.main
from anki.lang import _
from aqt import mw
from aqt.utils import tooltip, showText
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .preferences import get_preference, set_preference

assert isinstance(mw, aqt.main.AnkiQt)


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super(PreferencesDialog, self).__init__(parent)

        # initialize the table model and view
        self._table_model, self._table_view = self._prepare_table_model_and_view()

        if get_preference('deck_to_ease'):
            table_rows = [
                {"Deck" : deck, "Ease" : ease}
                for deck, ease in get_preference('deck_to_ease').items()
            ]
            for row in table_rows:
                self._append_row_data(row)

        self.resize(500, 300)
        self.setWindowTitle('Reset Ease - Preferences')
        self.vbox = QVBoxLayout(self)

        # add spacing
        self.vbox.addSpacing(20)

        # add table
        self.vbox.addWidget(self._table_view)

        # add QHboxLlayout
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)

        # add buttons
        self.add = make_button("Add", self._on_add, hbox)
        self.clone = make_button("Clone", self._on_clone, hbox)
        self.delete = make_button("Delete", self._on_delete, hbox)
        self.up = make_button("Up", self._on_up, hbox)
        self.down = make_button("Down", self._on_down, hbox)

        self._add_apply_and_cancel_buttons()

        self.setLayout(self.vbox)     

    def _prepare_table_model_and_view(self):
        table_model = QStandardItemModel(0, 2)
        table_view = QTableView()
        table_view.setModel(table_model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_model.setHeaderData(0, Qt.Horizontal, "Deck")
        table_model.setHeaderData(1, Qt.Horizontal, "Ease")
        return table_model, table_view

    def _add_apply_and_cancel_buttons(self):
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)

        buttonCancel = QPushButton("&Cancel")
        hbox.addWidget(buttonCancel, 1, Qt.AlignRight)
        buttonCancel.setMaximumWidth(150)
        buttonCancel.clicked.connect(self._on_cancel)

        buttonOkay = QPushButton("&Apply")
        hbox.addWidget(buttonOkay)
        buttonOkay.setMaximumWidth(150)
        buttonOkay.clicked.connect(self._on_okay)


    def _on_cancel(self):
        self.close()

    def _on_okay(self):
        deck_to_ease = {
            row_data['Deck'] : row_data['Ease']
            for row_data in self._table_rows()
        }
        
        set_preference('deck_to_ease', deck_to_ease)
        self.close()

    def _on_add(self):
        data = {"Deck" : mw.col.decks.allNames()[0], "Ease" : 250}
        self._append_row_data(data)

    def _on_clone(self):
        data = self._table_rows()[self._current_row_idx()]
        self._append_row_data(data)

    def _on_delete(self):
        # do not allow to delete the last row
        if len(self._table_rows()) == 1:
            return
        row_to_delete = self._current_row_idx()
        self._table_model.removeRow(row_to_delete)

    def _on_up(self):
        row_idx = self._current_row_idx()
        self._move_row_up(row_idx)
        self._table_view.selectRow(row_idx - 1)

    def _on_down(self):
        # moving a row down means moving the next row up
        row_idx = self._current_row_idx()
        self._move_row_up(row_idx + 1)
        self._table_view.selectRow(row_idx + 1)


    def _current_row_idx(self):
        indexes = self._table_view.selectedIndexes()
        return 0 if len(indexes) == 0 else indexes[0].row()


    def _table_rows(self):
        # reads the data from the widgets in the table and returns it

        assert hasattr(self, "_table_view")

        def table_view_row_to_data_row(model_row):
            result = {}
            result['Deck'] = model_row[0].currentText()
            result['Ease'] = int(model_row[1].text())
            return result

        def table_view_row_at_idx(row_idx):
            return [
                self._table_view.indexWidget(self._table_model.index(row_idx, col_idx))
                for col_idx in range(self._table_view.model().columnCount())
            ]

        return [
            table_view_row_to_data_row(table_view_row_at_idx(row_idx))
            for row_idx in range(self._table_view.model().rowCount())
        ]

    def _set_table_row(self, row_idx, row_data):
        # creates a gui row from the data and updates the _table_view with it
        assert row_idx >= 0

        def prepare_gui_table_row():

            def prepare_deck_combo_box():
                result = QComboBox()
                options = mw.col.decks.allNames()
                result.addItems(options)
                result.setCurrentIndex(options.index(row_data['Deck']))
                return result

            result = {}
            result['deckComboBox'] = prepare_deck_combo_box()
            result['easeEntry'] = QLineEdit(str(row_data['Ease']))
            return result

        def set_column(col_idx, widget):
            self._table_view.setIndexWidget(self._table_model.index(row_idx, col_idx), widget)

        gui_table_row = prepare_gui_table_row()
        set_column(0, gui_table_row['deckComboBox'])
        set_column(1, gui_table_row['easeEntry'])

    def _append_row_data(self, row_data):
        num_rows = len(self._table_rows())
        self._table_model.setRowCount(num_rows + 1)
        self._set_table_row(num_rows, row_data)

    def _move_row_up(self, row_idx):

        # the first "less than" is because the first row can't be moved up
        if not 0 < row_idx < len(self._table_rows()):
            return

        # row at row_idx swaps place with row above
        upper_row = self._table_rows()[row_idx - 1]
        lower_row = self._table_rows()[row_idx]

        self._set_table_row(row_idx - 1, lower_row)
        self._set_table_row(row_idx, upper_row)


def make_button(txt, f, parent):
    b = QPushButton(txt)
    b.clicked.connect(f)
    parent.addWidget(b)
    return b

def main():
    mw.mm = PreferencesDialog(mw)
    mw.mm.show()
