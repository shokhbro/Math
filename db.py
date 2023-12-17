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

class DBManyToMany:
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
            CREATE TABLE IF NOT EXISTS Student (
                student_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Course (
                course_id INTEGER PRIMARY KEY,
                title TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Enrollment (
                enrollment_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                course_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES Student (student_id),
                FOREIGN KEY (course_id) REFERENCES Course (course_id)
            )
        ''')

        self.conn.commit()

    def insert_student(self, name):
        self.cursor.execute('INSERT INTO Student (name) VALUES (?)', (name,))
        self.conn.commit()

    def insert_course(self, title):
        self.cursor.execute('INSERT INTO Course (title) VALUES (?)', (title,))
        self.conn.commit()

    def enroll_student_in_course(self, student_id, course_id):
        self.cursor.execute('INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)',
                            (student_id, course_id))
        self.conn.commit()

    def get_student_courses(self, student_id):
        self.cursor.execute('''
            SELECT Student.name, Course.title
            FROM Student
            JOIN Enrollment ON Student.student_id = Enrollment.student_id
            JOIN Course ON Enrollment.course_id = Course.course_id
            WHERE Student.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()