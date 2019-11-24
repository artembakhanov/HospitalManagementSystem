import sys

import Model
import View


class Controller:
    def __init__(self):
        # Initializing the main window
        self.app = View.QApplication(sys.argv)
        self.main_window = View.App()
        self.main_window.show()

        # Adding functionality to buttons
        self.main_window.exe_button.clicked.connect(self.SQL_query)  # "Execute" button
        self.main_window.gen_data_button.clicked.connect(self.Generate_data)  # "Generate data" button

        # Connecting to SQL DB
        self.sql_db = Model.SQL()

        # Executing the app
        self.app.exec_()

    def Generate_data(self):
        self.sql_db.generate_data()

    def SQL_query(self):
        """Reads the input from Text Field and either outputs the requested query in form of a table
            or throws an error"""
        text = self.main_window.textEdit.toPlainText()

        result = self.sql_db.process_query(text)

        # дальше, смотря какой резалт, что-то делаем (либо ашыбка, либо таблица)

        # Снизу закомменченный шаблон для вывода таблицы
        # self.table = View.ResultTable()
        # self.table.fill()
        # self.table.show()


if __name__ == "__main__":
    controller = Controller()
