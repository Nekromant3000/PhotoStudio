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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photographers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            portfolio_link TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            photographer_id INTEGER,
            service_id INTEGER,
            booking_date TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (photographer_id) REFERENCES photographers (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')

    conn.commit()
    conn.close()
    print('[DB] Все 4 таблицы успешно проверены/созданы.')

def seed_data():
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO services (title, price) VALUES ('Фото с животными', 5000)")
        cursor.execute("INSERT INTO services (title, price) VALUES ('Свадебная съемка', 15000)")
        cursor.execute("INSERT INTO services (title, price) VALUES ('Портрет', 3000)")
        
        cursor.execute("INSERT INTO photographers (name, specialization, portfolio_link) VALUES ('Анна', 'Свадьбы', 'C:/photos/anna')")
        cursor.execute("INSERT INTO photographers (name, specialization, portfolio_link) VALUES ('Олег', 'Животные', 'C:/photos/oleg')")
        
        conn.commit()
        print('[DB] Тестовые фотографы и услуги добавлены.')

    conn.close()

def add_client(name, phone):

    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO clients (name, phone)
        VALUES (?, ?)
    ''', (name, phone))

    conn.commit()
    conn.close()
    print(f"[DB] Запись добавлена: {name}, {phone}")

def get_all_clients():
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients')

    clients_data = cursor.fetchall()

    conn.close()
    return clients_data

def delete_client(client_id):
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))

    conn.commit()
    conn.close()
    print(f"[DB] Клиент с ID {client_id} удалён.")

def update_client(client_id, new_name, new_phone):
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE clients
        SET name = ?, phone = ?
        WHERE id = ?
    ''', (new_name, new_phone, client_id))

    conn.commit()
    conn.close()
    print(f"[DB] Данные клиента с ID {client_id} обновлены.")

def get_all_photographers():
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM photographers")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_services():
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM services")
    data = cursor.fetchall()
    conn.close()
    return data

def add_booking(client_id, photographer_id, service_id, date):
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO bookings (client_id, photographer_id, service_id, booking_date)
        VALUES (?, ?, ?, ?)
    ''', (client_id, photographer_id, service_id, date))

    conn.commit()
    conn.close()
    print(f"[DB] Запись на {date} успешно создана.")

def get_all_bookings():
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT
            bookings.id,
            clients.name,
            photographers.name,
            services.title,
            bookings.booking_date
        FROM bookings
        JOIN clients ON bookings.client_id = clients.id
        JOIN photographers ON bookings.photographer_id = photographers.id
        JOIN services ON bookings.service_id = services.id
    ''')

    data = cursor.fetchall()
    conn.close()
    return data

def delete_booking(booking_id):
    conn = sqlite3.connect("photostudio.db")
    cursor = conn.cursor()

    cursor.execute('DELETE FROM bookings WHERE id = ?', booking_id)

    conn.commit()
    conn.close()
    print(f"[DB] Запись с ID {booking_id} отменена.")

if __name__ == '__main__':
    create_tables()
    seed_data()