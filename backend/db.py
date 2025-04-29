import sqlite3
import csv
import bcrypt
conn = sqlite3.connect("eryx.db")
cursor = conn.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VACHAR(1000))"

# cursor.execute(query)
# # query = "INSERT INTO sys_command VALUES (null,'word', 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.EXE')"
# # cursor.execute(query)
# # conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))"
# cursor.execute(query)
# query = "INSERT INTO web_command VALUES (null,'github', 'https://github.com/')"
# cursor.execute(query)
# conn.commit()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS contacts (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(200) NOT NULL,
#     mobile_no VARCHAR(255) NOT NULL,
#     email VARCHAR(255)
# )
# ''')
# conn.commit()
# desired_columns_indices = [0, 18]  # Indices for the name and mobile_no columns in the CSV

# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         # Ensure the row has enough columns to extract
#         if len(row) > max(desired_columns_indices):
#             # Select the data from the desired columns (name and mobile_no)
#             selected_data = [row[i] for i in desired_columns_indices]
            
#             # Insert into the contacts table, skipping the 'id' as it's auto-incremented
#             cursor.execute('''INSERT INTO contacts (name, mobile_no) VALUES (?, ?);''', tuple(selected_data))

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# If want to insert single contact directly
# query = "INSERT INTO contacts VALUES (null,'sss', '', NULL)"
# cursor.execute(query)
# conn.commit()

# query = 'sakshi'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()

# # Print the result (mobile number)
# if results:
#     print(results[0][0])
# else:
#     print("No results found.")

# # Close the connection
# conn.close()

# query = "INSERT INTO contacts (name, mobile_no) VALUES ('Sakshi', '78780 42673')"
# cursor.execute(query)

# # Commit the transaction
# conn.commit()

# # Close the connection
# conn.close()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT NOT NULL UNIQUE,
#     password_hash TEXT NOT NULL
# )
# ''')
# conn.commit()

def register_user(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False