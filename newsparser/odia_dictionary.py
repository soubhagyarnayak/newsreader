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

    def getMeaning(self, word):
        pass

    def getStats(self):
        sqlText = '''SELECT COUNT(*) FROM OdiaDictionary'''
        cursor = self.db_conn.cursor()
        cursor.execute(sqlText)
        result = cursor.fetchone()
        return result[0]

    def putMeaningIfMissing(self, word, meaning='', type=''):
        sqlText = '''INSERT OR IGNORE INTO OdiaDictionary VALUES (?,?,?)'''
        cursor = self.db_conn.cursor()
        cursor.execute(sqlText, (word, meaning, type))
        self.db_conn.commit()

    def createTable(self):
        cursor = self.db_conn.cursor()
        sqlText = '''CREATE TABLE OdiaDictionary (word text PRIMARY KEY,
         meaning text, type text)'''
        cursor.execute(sqlText)
        self.db_conn.commit()
