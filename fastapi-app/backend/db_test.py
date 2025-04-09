import sqlite3

# Example: Connecting to a database
conn = sqlite3.connect('db/fastapi_db.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')

# Insert a record
cursor.execute('''INSERT INTO users (name) VALUES (?)''', ('John Doe',))
conn.commit()

# Fetch data
cursor.execute('SELECT * FROM users')
print(cursor.fetchall())

# Close connection
conn.close()
