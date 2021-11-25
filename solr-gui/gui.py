from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from solr import *


class Result(QListWidgetItem):
    def __init__(self, doc_id, title, author):
        super().__init__()

        content = str(doc_id) + "\t" + str(title) + "\t" + str(author)
        self.setText(content)


class GUI(QWidget):

    def __init__(self):
        super().__init__()

        server_label = QLabel('Server address:')
        self.server_address = QLineEdit('http://localhost:8983/solr/hsc-data/')

        param_label = QLabel('Search parameters:')
        self.search_box = QLineEdit()
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.search)
        self.fuzzy_toggle = QCheckBox('Fuzzy')

        results_label = QLabel('Results:')
        self.results = QListWidget()
        self.results = QTableWidget()
        self.results.setColumnCount(3)
        self.results.setColumnWidth(0, 50)
        self.results.setColumnWidth(1, 250)
        self.results.setColumnWidth(2, 250)
        self.results.setRowCount(20)
        self.results.setHorizontalHeaderLabels(['ID', 'Title(s)', 'Author(s)'])

        layout = QGridLayout()
        layout.addWidget(server_label, 0, 0)
        layout.addWidget(self.server_address, 0, 1)

        layout.addWidget(param_label, 1, 0)
        layout.addWidget(self.search_box, 1, 1)
        layout.addWidget(self.search_btn, 1, 2)
        layout.addWidget(self.fuzzy_toggle, 1, 3)

        layout.addWidget(results_label, 2, 0)
        layout.addWidget(self.results, 3, 0, 32, 3)

        self.setLayout(layout)

    def search(self):
        server = self.server_address.text()
        query = self.search_box.text()
        fuzzy = self.fuzzy_toggle.isDown()

        docs = solr_search(server, query, fuzzy)

        self.results.clear()
        for row_index, doc in enumerate(docs):
            doc_id = QTableWidgetItem(str(doc['id']))
            doc_id.setFlags(doc_id.flags() & ~Qt.ItemIsEditable)
            self.results.setItem(row_index, 0, doc_id)

            title = QTableWidgetItem(str(doc['title']))
            title.setFlags(title.flags() & ~Qt.ItemIsEditable)
            self.results.setItem(row_index, 1, title)

            author = QTableWidgetItem(str(doc['author']))
            author.setFlags(author.flags() & ~Qt.ItemIsEditable)
            self.results.setItem(row_index, 2, author)


