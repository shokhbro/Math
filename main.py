import sqlite3

# SQLite bilan bog'liq test ma'lumotlar bazasiga ulanish
connection = sqlite3.connect("sqlite_db/test.db")

# kursor obyekti yaratish
cursor = connection.cursor()

# SQL so'rovlar orqali table yaratish
cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

# Yangi foydalanuvchi ma'lumotlarini so'rang
new_name = input("Ismingizni kiriting: ")
new_age = int(input("Yoshingizni kiriting: "))

# Bazaga ma'lumot qo'shish
cursor.execute('INSERT INTO Users (name, age) VALUES (?, ?)', (new_name, new_age))

# Bazadan malumot olish
cursor.execute(''' SELECT * FROM Users  ''')

# Natijani ko'rish
result = cursor.fetchall()
print(result)

# Bazaga o'zgartirishlar saqlash
connection.commit()
# Bazadan chiqish
connection.close()

