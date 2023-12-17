import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student (
        student_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Course (
        course_id INTEGER PRIMARY KEY,
        title TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollment (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Student (student_id),
        FOREIGN KEY (course_id) REFERENCES Course (course_id)
    )
''')

# Insert sample data
cursor.execute('INSERT INTO Student (name) VALUES (?)', ('John Doe',))
cursor.execute('INSERT INTO Student (name) VALUES (?)', ('Jane Smith',))

cursor.execute('INSERT INTO Course (title) VALUES (?)', ('Math 101',))
cursor.execute('INSERT INTO Course (title) VALUES (?)', ('History 101',))

cursor.execute('INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)', (1, 1))  # John Doe enrolls in Math 101
cursor.execute('INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)', (1, 2))  # John Doe enrolls in History 101
cursor.execute('INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)', (2, 2))  # Jane Smith enrolls in History 101

# Commit the changes
conn.commit()

# Query the data
cursor.execute('''
    SELECT Student.name AS student, Course.title AS course
    FROM Student
    JOIN Enrollment ON Student.student_id = Enrollment.student_id
    JOIN Course ON Enrollment.course_id = Course.course_id
''')

results = cursor.fetchall()
for result in results:
    print(result)

# Close the connection
conn.close()
