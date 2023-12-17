import sqlite3

class DBOneToMany:
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
            CREATE TABLE IF NOT EXISTS Department (
                department_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
                employee_id INTEGER PRIMARY KEY,
                name TEXT,
                salary REAL,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES Department (department_id)
            )
        ''')

        self.conn.commit()

    def insert_department(self, name):
        self.cursor.execute('INSERT INTO Department (name) VALUES (?)', (name,))
        self.conn.commit()

    def insert_employee(self, name, salary, department_id):
        self.cursor.execute('INSERT INTO Employee (name, salary, department_id) VALUES (?, ?, ?)',
                            (name, salary, department_id))
        self.conn.commit()

    def get_department_employees(self, department_id):
        self.cursor.execute('''
            SELECT Department.name AS department, Employee.name AS employee, Employee.salary
            FROM Department
            LEFT JOIN Employee ON Department.department_id = Employee.department_id
            WHERE Department.department_id = ?
        ''', (department_id,))
        return self.cursor.fetchall()

# Example usage:
db_one_to_many = DBOneToMany()
db_one_to_many.connect()
db_one_to_many.create_tables()
db_one_to_many.insert_department('IT')
db_one_to_many.insert_department('HR')
db_one_to_many.insert_employee('John Doe', 50000, 1)
db_one_to_many.insert_employee('Jane Smith', 60000, 1)
db_one_to_many.insert_employee('Bob Johnson', 55000, 2)
result = db_one_to_many.get_department_employees(1)
print(result)

db_one_to_many.disconnect()
