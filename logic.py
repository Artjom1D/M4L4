import sqlite3
import pandas as pd

from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS favorite (
                        channel_id INTEGER PRIMARY KEY NOT NULL,
                        channel_name TEXT NOT NULL,
                        channel_language TEXT NOT NULL,
                        bot_tema TEXT NOT NULL,
                        FOREIGN KEY(channel_name) REFERENCES dataset(Channel),
                        FOREIGN KEY(channel_language) REFERENCES dataset(Language)
                    )''') 

            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
    
    def add_favorite(self, name, bot_tema="general"):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT Channel, Language FROM dataset WHERE Channel = ?", (name,))
            result = cur.fetchone()

            if result:
                channel, language = result
                cur.execute("""
                    INSERT INTO favorite (channel_name, channel_language, bot_tema)
                    VALUES (?, ?, ?)
                """, (channel, language, bot_tema))
                print(f"Добавлено в избранное: {channel}")
            else:
                print("Канал не найден в dataset")

    def delete(self, name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM favorite WHERE channel_name = ?", (name,))
            if cur.rowcount > 0:
                return f"Канал '{name}' удалён из избранного."
            else:
                return f"Канал '{name}' не найден в избранном."


    def my_favorites(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT channel_name FROM favorite")
            rows = cur.fetchall()
            return [r[0] for r in rows]

    def find_acc(self, name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT Channel FROM dataset WHERE Channel LIKE ?", (f"%{name}%",))
            rows = cur.fetchall()
            return [r[0] for r in rows]
    
    def infok(self, name):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM dataset WHERE Channel LIKE ?", (f"%{name}%",))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            return rows, columns
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)