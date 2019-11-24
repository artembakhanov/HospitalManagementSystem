from PyQt5.QtWidgets import *
import design


class App(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = self.setupUi(self)


class ResultTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def fill(self, result):
        self.table_widget.clear()

        labels = result.column_names

        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        for row in result.values:
            table_row = self.table_widget.rowCount()
            self.table_widget.setRowCount(table_row + 1)
            for i in range(len(row)):
                self.table_widget.setItem(table_row, i, QTableWidgetItem(str(row[i])))
        # for id_, name, price in [(1, 'a', 23), (2, 'b', 24)]:
        #     row = self.table_widget.rowCount()
        #     self.table_widget.setRowCount(row + 1)
        #
        #     self.table_widget.setItem(row, 0, QTableWidgetItem(str(id_)))
        #     self.table_widget.setItem(row, 1, QTableWidgetItem(name))
        #     self.table_widget.setItem(row, 2, QTableWidgetItem(price))
