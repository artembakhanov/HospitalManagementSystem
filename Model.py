import psycopg2


class SQL:
    def __init__(self):
        # connect to DB
        # АРТЕМ ПОМЕНЯЙ ЭТО НА КОННЕКТ ТУ ДАМБ
        # Я ПОМЕНЯЮ СПАСИБО
        self.conn = psycopg2.connect(
            database='scp',
            user='postgres',
            password='root1234'
        )

        print('Connected successfully')

    def process_query(self, query):
        """Takes an SQL query and processes it"""
        cur = self.conn.cursor()

        # в query хранится текст, который юзер ввел
        # заимплементь функцию

        # внизу пример того, как я со своей дб таблицу считывал
        """
        rows = []

        try:
            cur.execute("SELECT * FROM catalog")
            rows = cur.fetchall()
        except Exception:
            print("ERROR")

        for row in rows:
            print(row)"""
