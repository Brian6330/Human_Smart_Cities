import sys
from typing import AnyStr

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

from solr import *


class SearchResult(QListWidgetItem):
    def __init__(self, doc_id: AnyStr, title: AnyStr, author: AnyStr):
        super().__init__()

        content = str(doc_id) + "\t" + str(title) + "\t" + str(author)
        self.setText(content)


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        ROW = 0

        layout = QGridLayout()

        self.server_address = QLineEdit('http://localhost:8983/solr/hsc-data/')
        layout.addWidget(QLabel('Server address:'), ROW, 0)
        layout.addWidget(self.server_address, ROW, 1)
        ROW += 1

        self.search_box = QLineEdit()
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.search)
        self.fuzzy_toggle = QCheckBox('Fuzzy')
        layout.addWidget(QLabel('Search parameters:'), 1, 0)
        layout.addWidget(self.search_box, ROW, 1)
        layout.addWidget(self.search_btn, ROW, 2)
        layout.addWidget(self.fuzzy_toggle, ROW, 3)
        ROW += 1

        self.search_results = QTableWidget()
        self.search_results.setColumnCount(3)
        self.search_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.search_results.setHorizontalHeaderLabels(['ID', 'Title(s)', 'Author(s)'])
        layout.addWidget(QLabel('Results:'), ROW, 0)
        ROW += 1
        layout.addWidget(self.search_results, ROW, 0, 20, 4)
        ROW += 1

        self.experts = QTableWidget()

        self.setLayout(layout)

    def search(self):
        server = self.server_address.text()
        query = self.search_box.text()
        fuzzy = self.fuzzy_toggle.isChecked()

        docs = solr_search(server, query, fuzzy)

        # unneeded as we overwrite cell contents after setting row count
        # self.results.clearContents()
        self.search_results.setRowCount(len(docs))
        for row_index, doc in enumerate(docs):
            doc_id = QTableWidgetItem(str(doc['id']))
            doc_id.setFlags(doc_id.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 0, doc_id)

            title_str = ', '.join(doc.get('title', []))
            title = QTableWidgetItem(title_str)
            title.setFlags(title.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 1, title)

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
