import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

from solr import *


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.__setup_widgets__()
        self.__setup_layout__()
        self.__setup_connections__()

    def __setup_widgets__(self) -> None:
        """
        Creates widgets:
        - server address input field
        - search box input field
        - search button
        - fuzzy search toggle button
        - search results table
        - expert results table
        :return:
        """
        self.server_address = QLineEdit('http://localhost:8983/solr/hsc-data/')

        self.search_box = QLineEdit()
        self.search_btn = QPushButton('Search')
        self.fuzzy_toggle = QCheckBox('Fuzzy')

        self.search_results = QTableWidget()
        self.search_results.setColumnCount(3)
        self.search_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.search_results.setHorizontalHeaderLabels(['ID', 'Title(s)', 'Author(s)'])

        self.experts = QTableWidget()

    def __setup_layout__(self) -> None:
        """
        Creates the layout with all widgets.
        :return:
        """
        layout = QGridLayout()
        ROW = 0
        layout.addWidget(QLabel('Server address:'), ROW, 0)
        layout.addWidget(self.server_address, ROW, 1)
        ROW += 1
        layout.addWidget(QLabel('Search parameters:'), 1, 0)
        layout.addWidget(self.search_box, ROW, 1)
        layout.addWidget(self.search_btn, ROW, 2)
        layout.addWidget(self.fuzzy_toggle, ROW, 3)
        ROW += 1
        layout.addWidget(QLabel('Results:'), ROW, 0)
        ROW += 1
        layout.addWidget(self.search_results, ROW, 0, 20, 4)
        ROW += 1

        # TODO: add experts

        self.setLayout(layout)

    def __setup_connections__(self):
        """
        Connects button presses to events like
        - tab selects next field
        - search button
        :return:
        """
        self.search_box.returnPressed.connect(self.search)
        self.search_btn.clicked.connect(self.search)

    def search(self):
        server = self.server_address.text()
        query = self.search_box.text()
        fuzzy = self.fuzzy_toggle.isChecked()

        docs = solr_search(server, query, fuzzy)

        # unneeded as we overwrite cell contents after setting row count
        # self.results.clearContents()
        self.search_results.setRowCount(len(docs))
        for row_index, doc in enumerate(docs):
            # set ID
            doc_id = QTableWidgetItem(str(doc['id']))
            doc_id.setFlags(doc_id.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 0, doc_id)

            # set TITLE
            title_str = ', '.join(doc.get('title', []))
            title = QTableWidgetItem(title_str)
            title.setFlags(title.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 1, title)

            # set AUTHORS
            authors = doc.get('author', [])
            if authors is list:
                author_str = ', '.join(authors)
            else:
                author_str = str(authors)
            author = QTableWidgetItem(author_str)
            author.setFlags(author.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 2, author)


if __name__ == "__main__":
    app = QApplication([])

    widget = GUI()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
