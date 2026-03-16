import sqlite3


'''
The class acts as a wrapper over a SQLite DB
'''


class OdiaDictionary:
    def __init__(self, db_path='./odia_dictionary.db'):
        self.db_path = db_path

    def __enter__(self):
        self.db_conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_conn.close()

    def get_meaning(self, word):
        pass

    def get_stats(self):
        sql = 'SELECT COUNT(*) FROM OdiaDictionary'
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]

    def put_meaning_if_missing(self, word, meaning='', word_type=''):
        sql = 'INSERT OR IGNORE INTO OdiaDictionary VALUES (?,?,?)'
        cursor = self.db_conn.cursor()
        cursor.execute(sql, (word, meaning, word_type))
        self.db_conn.commit()

    def create_table(self):
        cursor = self.db_conn.cursor()
        sql = '''CREATE TABLE OdiaDictionary (word text PRIMARY KEY,
         meaning text, type text)'''
        cursor.execute(sql)
        self.db_conn.commit()
