import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

from scripts.expert_finder import search_for_keyword
from scripts.keyword_counter import determine_keywords
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

        # self.experts = QListWidget()
        self.experts = QTableWidget()
        self.experts.setColumnCount(2)
        self.experts.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.experts.setHorizontalHeaderLabels(['Score', 'Author(s)'])

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
        layout.addWidget(self.search_results, ROW, 0, 10, 4)
        ROW += 10
        layout.addWidget(QLabel('Experts (best match first):'), ROW, 0)
        ROW += 1
        layout.addWidget(self.experts, ROW, 0, 5, 4)
        ROW += 1

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
            score = QTableWidgetItem(str(doc['id']))
            score.setFlags(score.flags() & ~Qt.ItemIsEditable)
            self.search_results.setItem(row_index, 0, score)

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

        results = determine_keywords(docs)
        experts = search_for_keyword(results, search_term=query)

        self.experts.setRowCount(len(experts))
        for row_index, (expert, score) in enumerate(experts):
            # set SCORE
            score = QTableWidgetItem(str(score))
            score.setFlags(score.flags() & ~Qt.ItemIsEditable)
            self.experts.setItem(row_index, 0, score)

            # set EXPERT
            expert = QTableWidgetItem(str(expert))
            expert.setFlags(score.flags() & ~Qt.ItemIsEditable)
            self.experts.setItem(row_index, 1, expert)


if __name__ == "__main__":
    app = QApplication([])

    widget = GUI()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
