import sys

from PyQt5.QtCore import QPointF

import Model
import View
from static import QUERY1, QUERY2, QUERY3, QUERY4, QUERY5


class Controller:
    def __init__(self):
        # Initializing the main window
        self.app = View.QApplication(sys.argv)
        self.main_window = View.App()
        self.main_window.show()

        # Adding functionality to buttons
        self.main_window.exe_button.clicked.connect(self.SQL_query)  # "Execute" button
        self.main_window.gen_data_button.clicked.connect(self.Generate_data)  # "Generate data" button
        self.main_window.def_q1_button.clicked.connect(self.query1)
        self.main_window.def_q2_button.clicked.connect(self.query2)
        self.main_window.def_q3_button.clicked.connect(self.query3)
        self.main_window.def_q4_button.clicked.connect(self.query4)
        self.main_window.def_q5_button.clicked.connect(self.query5)

        # Connecting to SQL DB
        self.sql_db = Model.SQL()

        # Executing the app
        self.app.exec_()

    def Generate_data(self):
        self.sql_db.populate_database()

    def SQL_query(self):
        """Reads the input from Text Field and either outputs the requested query in form of a table
            or throws an error"""
        text = self.main_window.textEdit.toPlainText()

        result = self.sql_db.process_query(text)

        if not result.is_error:
            self.table = View.ResultTable()
            self.table.fill(result)
            self.table.resize(1920, 1080)
            self.table.show()
        else:
            self.main_window.error_dialog_box(str(result.exception))
            
        # print(result)

    def query1(self):
        self.main_window.textEdit.setText(QUERY1)

    def query2(self):
        self.main_window.textEdit.setText(QUERY2)

    def query3(self):
        self.main_window.textEdit.setText(QUERY3)

    def query4(self):
        self.main_window.textEdit.setText(QUERY4)

    def query5(self):
        self.main_window.textEdit.setText(QUERY5)


if __name__ == "__main__":
    controller = Controller()
