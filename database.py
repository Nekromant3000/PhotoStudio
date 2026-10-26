import sqlite3

def create_tables():
    conn = sqlite3.connect('photostudio.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print('База данных и таблица клиентов успешно созданы!')

if __name__ == '__main__':
    create_tables()