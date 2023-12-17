import sqlite3

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

# Example usage:
db_many_to_many = DBManyToMany()
db_many_to_many.connect()
db_many_to_many.create_tables()
db_many_to_many.insert_student('John Doe')
db_many_to_many.insert_student('Jane Smith')
db_many_to_many.insert_course('Math 101')
db_many_to_many.insert_course('History 101')
db_many_to_many.enroll_student_in_course(1, 1)  # John Doe enrolls in Math 101
db_many_to_many.enroll_student_in_course(1, 2)  # John Doe enrolls in History 101
db_many_to_many.enroll_student_in_course(2, 2)  # Jane Smith enrolls in History 101
result = db_many_to_many.get_student_courses(1)
print(result)
for i in result:
    print(i)
db_many_to_many.disconnect()
