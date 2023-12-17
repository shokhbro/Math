import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Person (
        person_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Passport (
        passport_id INTEGER PRIMARY KEY,
        passport_number TEXT UNIQUE,
        expiry_date DATE,
        person_id INTEGER UNIQUE,
        FOREIGN KEY (person_id) REFERENCES Person (person_id)
    )
''')

# Insert sample data
cursor.execute('INSERT INTO Person (name, age) VALUES (?, ?)', ('John Doe', 30))
cursor.execute('INSERT INTO Passport (passport_number, expiry_date, person_id) VALUES (?, ?, ?)', ('ABC123', '2025-12-31', 1))

# Commit the changes
conn.commit()

# Query the data
cursor.execute('''
    SELECT Person.name, Person.age, Passport.passport_number, Passport.expiry_date
    FROM Person
    JOIN Passport ON Person.person_id = Passport.person_id
''')

result = cursor.fetchone()
print(result)

# Close the connection
conn.close()

