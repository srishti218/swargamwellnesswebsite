import sqlite3

# Connect to the database
conn = sqlite3.connect('education_visits.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Query data
cursor.execute("SELECT * FROM EducationVisit;")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()