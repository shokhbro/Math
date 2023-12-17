import sqlite3

class MisolDB:
    def __init__(self, db_name='sqlite_db/misol.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_tables(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Oyinchi (
                id INTEGER PRIMARY KEY,
                ism TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Natijalar (
                id INTEGER PRIMARY KEY,
                oyinchi_id INTEGER,
                togri INTEGER,
                notogri INTEGER,
                FOREIGN KEY (oyinchi_id) REFERENCES Oyinchi (id)
            )
        ''')
        self.disconnect()

    def insert_oyinchi(self, ism):
        self.connect()
        self.cursor.execute('INSERT INTO Oyinchi (ism) VALUES (?)', (ism,))
        oyinchi_id = self.cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        return oyinchi_id

    def insert_natija(self, oyinchi_id, togri, notogri):
        self.connect()
        self.cursor.execute('INSERT INTO Natijalar (oyinchi_id, togri, notogri) VALUES (?, ?, ?)',
                            (oyinchi_id, togri, notogri))
        self.conn.commit()
        self.disconnect()

    def get_all_natijalar(self):
        self.connect()
        self.cursor.execute('''
            SELECT Oyinchi.ism, SUM(Natijalar.togri) AS top, SUM(Natijalar.notogri) AS top
            FROM Oyinchi
            LEFT JOIN Natijalar ON Oyinchi.id = Natijalar.oyinchi_id
            GROUP BY Oyinchi.ism
            ORDER BY top DESC
        ''')
        natijalar = self.cursor.fetchall()
        self.disconnect()
        return natijalar

