import sqlite3
import os


class DbTextAnalyser:
    """Class contain provide object db for TextAnalyser tool with methods to manage db"""
    def __init__(self, path='vocabulary.db'):
        self.path = path
        self.wTable = 'words'

        self.con = None
        self.cur = None
        self.initiate_connection()
        self.create_words_t()

    def initiate_connection(self):
        """Initiate connection to db"""
        if os.path.exists(self.path) is True:
            print("db exists")
        if os.path.exists(self.path) is False:
            print("db is not exists, create db")
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        print(F'connected to {self.con}')

    def close_db_connection(self):
        """Close connection to db"""
        self.con.close()

    def create_words_t(self):
        # Spending tables creation
        sql = (F"create table if not exists {self.wTable} (id, name, speach_part,"
               F"translations, definition, importance, topic)")
        self.cur.execute(sql)

    def add_record_words_t(self, name, speach_part, translation, definition, importance, topic):
        """Add record to word table"""
        sql = F"SELECT COUNT(*) as count FROM {self.wTable}"
        self.cur.execute(sql)
        item_id = self.cur.fetchone()[0] + 1
        sql = (F"INSERT INTO {self.wTable} VALUES ({item_id}, '{name}', '{speach_part}',"
               F"'{translation}', '{definition}', '{importance}', '{topic}')")
        self.cur.execute(sql)
        self.con.commit()

    def remove_record_words_t_by_id(self, item_id):
        """Remove record from word table by given id"""
        sql = F"DELETE FROM {self.wTable} WHERE id = {int(item_id)}"
        self.cur.execute(sql)
        self.con.commit()

    def get_columns_names(self, table):
        """Get column names from given table"""
        sql = F"pragma table_info({table})"
        self.cur.execute(sql)
        col_names = []
        for el in self.cur.fetchall():
            col_names.append(el[1])
        return col_names

    def get_records(self, table):
        """Get all records from given table"""
        if table == 'words':
            sql = F"SELECT * FROM {self.wTable}"
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data


if __name__ == '__main__':
    db_text_analyser = DbTextAnalyser()
    # db_text_analyser.add_record_words_t('fine', 'noun', 'штраф, пеня',
    # 'The fine an amount of money that has to be paid as a punishment for not obeying a rule or law', 5, 'setup')
    # print(db_text_analyser.get_records('words'))
    # db_text_analyser.remove_record_words_t_by_id(1)
    print(db_text_analyser.get_records('words'))
    db_text_analyser.close_db_connection()
