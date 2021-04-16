from abc import abstractmethod

from anki.lang import _
from aqt import mw
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TableDialog(QDialog):
    def __init__(self, parent=None):
        super(TableDialog, self).__init__(parent)

        # initialize the table model and view
        self._table_model, self._table_view = self._prepare_table_model_and_view()

        rows = self._rows_at_start()
        assert all([len(row) == len(self.col_names) for row in rows])
        for row in rows:
            self._append_row(row)

        self.resize(500, 300)
        self.setWindowTitle(self.window_title)
        self.vbox = QVBoxLayout(self)

        label = QLabel(self.description)

        label.setWordWrap(True)
        font = label.font()
        font.setPixelSize(10)
        label.setFont(font)
        self.vbox.addWidget(label)

        # add table
        self.vbox.addWidget(self._table_view)

        # add QHboxLlayout
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)

        # add buttons
        self.add = make_button("Add", self._on_add, hbox)
        self.delete = make_button("Delete", self._on_delete, hbox)
        self.up = make_button("Up", self._on_up, hbox)
        self.down = make_button("Down", self._on_down, hbox)

        self._add_apply_and_cancel_buttons()

        self.setLayout(self.vbox)     

    @abstractmethod
    def _rows_at_start(self):
        pass

    @abstractmethod
    def _save_preferences(self):
        pass

    @abstractmethod
    def _default_row(self):
        pass

    @abstractmethod
    def _data_row_to_gui_row(self, data_row):
        pass

    @abstractmethod
    def _gui_row_to_data_row(self, gui_row):
        pass


    def _prepare_table_model_and_view(self):
        table_model = QStandardItemModel(0, len(self.col_names))
        table_view = QTableView()
        table_view.setModel(table_model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        for i, col_name in enumerate(self.col_names):
            table_model.setHeaderData(i, Qt.Horizontal, col_name)

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
        self._save_preferences(self._rows())

    def _on_add(self):
        self._append_row(self._default_row())

    def _on_delete(self):
        if len(self._rows()) == 0:
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


    def _rows(self):
        # reads the data from the widgets in the table and returns it

        assert hasattr(self, "_table_view")

        def gui_row_at_idx(row_idx):
            return [
                self._table_view.indexWidget(self._table_model.index(row_idx, col_idx))
                for col_idx in range(self._table_view.model().columnCount())
            ]

        return [
            self._gui_row_to_data_row(gui_row_at_idx(row_idx))
            for row_idx in range(self._table_view.model().rowCount())
        ]


    def _set_row(self, row_idx, data_row):
        # creates a gui row from the data and updates the _table_view with it
        assert row_idx >= 0

        def set_column(col_idx, widget):
            self._table_view.setIndexWidget(self._table_model.index(row_idx, col_idx), widget)

        gui_row = self._data_row_to_gui_row(data_row)
        for i in range(len(self.col_names)):
            set_column(i, gui_row[i])

    def _append_row(self, data_row):
        num_rows = len(self._rows())
        self._table_model.setRowCount(num_rows + 1)
        self._set_row(num_rows, data_row)

    def _move_row_up(self, row_idx):

        # the first "less than" is because the first row can't be moved up
        if not 0 < row_idx < len(self._rows()):
            return

        # row at row_idx swaps place with row above
        upper_row = self._rows()[row_idx - 1]
        lower_row = self._rows()[row_idx]

        self._set_row(row_idx - 1, lower_row)
        self._set_row(row_idx, upper_row)


def make_button(txt, f, parent):
    b = QPushButton(txt)
    b.clicked.connect(f)
    parent.addWidget(b)
    return b
