import sqlite3

# Connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date TEXT NOT NULL
)
''')

# Insert a record
cursor.execute('''
INSERT INTO users (username, email, registration_date)
VALUES ('johndoe', 'johndoe@example.com', '2024-07-22')
''')

# Commit the transaction
conn.commit()

# Query the database
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
