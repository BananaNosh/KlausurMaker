import sqlite3


TRANSLATION_TABLE = "translation_table"
LEMMA_ADDS_TABLE = "lemma_adds_table"
WORD_KEY = "word"
LEMMA_KEY = "lemma"
ADDS_KEY = "adds"
TRANSLATION_KEY ="translation"


class DatabaseManager:
    def __init__(self, db_name="vocabs.db"):
        self.conn = sqlite3.connect(db_name)

    def create_lemma_adds_table(self):
        cursor = self.conn.cursor()

        create_table = f"CREATE TABLE IF NOT EXISTS {LEMMA_ADDS_TABLE} " \
                       f"({WORD_KEY} text, {LEMMA_KEY} text, {ADDS_KEY} text, PRIMARY KEY ({WORD_KEY}))"
        cursor.execute(create_table)

        self.conn.commit()

    def create_translation_table(self):
        cursor = self.conn.cursor()

        create_table = f"CREATE TABLE IF NOT EXISTS {TRANSLATION_TABLE} " \
                       f"({LEMMA_KEY} text, {ADDS_KEY} text, {TRANSLATION_KEY} text, " \
                       f"CONSTRAINT lemma_adds PRIMARY KEY ({LEMMA_KEY}, {ADDS_KEY}))"
        cursor.execute(create_table)

        self.conn.commit()

    def insert_lemma_adds(self, word, lemma, adds):
        self.insert_lemma_adds_multiple([(word, lemma, adds)])

    def insert_lemma_adds_multiple(self, word_lemma_adds_list):
        """
        Insert into lemma_adds table
        Args:
            word_lemma_adds_list(list((str, str, str))): list of tuples of word, lemma and adds
        """
        self.create_lemma_adds_table()
        cursor = self.conn.cursor()

        for params in word_lemma_adds_list:
            try:
                insert = f"INSERT INTO {LEMMA_ADDS_TABLE} VALUES (?, ?, ?)"
                cursor.execute(insert, params)
            except sqlite3.IntegrityError:
                update = f"UPDATE {LEMMA_ADDS_TABLE} SET {LEMMA_KEY}=?, {ADDS_KEY}=? WHERE {WORD_KEY}=?"
                cursor.execute(update, (params[1], params[2], params[0]))

        self.conn.commit()

    def insert_translation(self, lemma, adds, translation):
        self.insert_translation_multiple([(lemma, adds, translation)])

    def insert_translation_multiple(self, lemma_adds_translation_list):
        """
        Insert into translation table
        Args:
            lemma_adds_translation_list(list((str, str, str))): list of tuples of lemma, adds and translation
        """
        self.create_translation_table()
        cursor = self.conn.cursor()

        for params in lemma_adds_translation_list:
            try:
                insert = f"INSERT INTO {TRANSLATION_TABLE} VALUES (?, ?, ?)"
                cursor.execute(insert, params)
            except sqlite3.IntegrityError:
                update = f"UPDATE {TRANSLATION_TABLE} SET {TRANSLATION_KEY}=? WHERE {LEMMA_KEY}=? and {ADDS_KEY}=?"
                cursor.execute(update, (params[2], params[0], params[1]))

        self.conn.commit()

    def retrieve_lemma_adds(self, word):
        return self.retrieve_lemma_adds_multiple([word])[0]

    def retrieve_lemma_adds_multiple(self, words):
        self.create_lemma_adds_table()
        cursor = self.conn.cursor()

        select = f"SELECT * FROM {LEMMA_ADDS_TABLE} WHERE {WORD_KEY}=?"

        result = []
        for word in words:
            cursor.execute(select, (word, ))
            row = cursor.fetchone()
            if row is None:
                row = (word, None, None)
            result.append(row)
        return result

    def retrieve_translation(self, lemma, adds):
        return self.retrieve_translation_multiple([(lemma, adds)])[0]

    def retrieve_translation_multiple(self, lemma_adds_list):
        self.create_translation_table()
        cursor = self.conn.cursor()

        select = f"SELECT * FROM {TRANSLATION_TABLE} WHERE {LEMMA_KEY}=? AND {ADDS_KEY}=?"

        result = []
        for params in lemma_adds_list:
            cursor.execute(select, params)
            row = cursor.fetchone()
            if row is None:
                row = (params[0], params[1], None)
            result.append(row)
        return result

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    manager = DatabaseManager("test_vocabs")
    manager.create_lemma_adds_table()
    manager.create_translation_table()
    manager.insert_lemma_adds_multiple([("wort1", "lemma1", "adds1"), ("wort2", "lemma2", "adds2"), ("wort3", "lemma3", "adds3")])
    print(manager.retrieve_lemma_adds_multiple(["wort1", "wort3", "wort5"]))
    manager.insert_lemma_adds_multiple([("wort1", "lemma13", "adds13"), ("wort4", "lemma4", "adds4"), ("wort2", "lemma2", "adds2"), ("wort1", "lemma14", "adds14")])
    print(manager.retrieve_lemma_adds_multiple(["wort1", "wort3", "wort2", "wort4"]))
    manager.insert_translation_multiple([("lemma1", "adds1", "trans1"), ("lemma2", "adds2", "trans2")])
    print(manager.retrieve_translation_multiple([("lemma2", "adds2"), ("lemma1", "adds3"), ("lemma1", "adds1"), ("lemma3", "adds3")]))
    manager.insert_translation_multiple([("lemma1", "adds13", "trans1"), ("lemma3", "adds3", "trans3")])
    print(manager.retrieve_translation_multiple([("lemma3", "adds3"), ("lemma1", "adds1"), ("lemma1", "adds13")]))
