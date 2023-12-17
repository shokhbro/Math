import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Department (
        department_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        salary REAL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES Department (department_id)
    )
''')

# Insert sample data
cursor.execute('INSERT INTO Department (name) VALUES (?)', ('IT',))
cursor.execute('INSERT INTO Department (name) VALUES (?)', ('HR',))

cursor.execute('INSERT INTO Employee (name, salary, department_id) VALUES (?, ?, ?)', ('John Doe', 50000, 1))
cursor.execute('INSERT INTO Employee (name, salary, department_id) VALUES (?, ?, ?)', ('Jane Smith', 60000, 1))
cursor.execute('INSERT INTO Employee (name, salary, department_id) VALUES (?, ?, ?)', ('Bob Johnson', 55000, 2))

# Commit the changes
conn.commit()

# Query the data
cursor.execute('''
    SELECT Department.name AS department, Employee.name AS employee, Employee.salary
    FROM Department
    LEFT JOIN Employee ON Department.department_id = Employee.department_id
''')

results = cursor.fetchall()
for result in results:
    print(result)

# Close the connection
conn.close()
