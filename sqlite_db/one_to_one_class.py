import sqlite3

class DBOneToOne:
    def __init__(self, db_name='example.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Person (
                person_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passport (
                passport_id INTEGER PRIMARY KEY,
                passport_number TEXT UNIQUE,
                expiry_date DATE,
                person_id INTEGER UNIQUE,
                FOREIGN KEY (person_id) REFERENCES Person (person_id)
            )
        ''')

        self.conn.commit()

    def insert_person(self, name, age):
        self.cursor.execute('INSERT INTO Person (name, age) VALUES (?, ?)', (name, age))
        self.conn.commit()

    def insert_passport(self, passport_number, expiry_date, person_id):
        self.cursor.execute('INSERT INTO Passport (passport_number, expiry_date, person_id) VALUES (?, ?, ?)',
                            (passport_number, expiry_date, person_id))
        self.conn.commit()

    def get_person_passport(self, person_id):
        self.cursor.execute('''
            SELECT Person.name, Person.age, Passport.passport_number, Passport.expiry_date
            FROM Person
            JOIN Passport ON Person.person_id = Passport.person_id
            WHERE Person.person_id = ?
        ''', (person_id,))
        return self.cursor.fetchone()

# Example usage:
db_one_to_one = DBOneToOne()
db_one_to_one.connect()
db_one_to_one.create_tables()
db_one_to_one.insert_person('John Doe', 30)
db_one_to_one.insert_passport('ABC123', '2025-12-31', 1)
result = db_one_to_one.get_person_passport(1)
print(result)
db_one_to_one.disconnect()
