from PyQt5.QtWidgets import *

import design


class App(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = self.setupUi(self)

    def error_dialog_box(self, exception):
        QMessageBox.about(self, "Exception", exception)


class ResultTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        # self.setWindowState(design.QtCore.Qt.WindowFullScreen)

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
