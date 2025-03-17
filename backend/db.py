import sqlite3

conn = sqlite3.connect("eryx.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VACHAR(1000))"

cursor.execute(query)
# query = "INSERT INTO sys_command VALUES (null,'word', 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.EXE')"
# cursor.execute(query)
# conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))"
cursor.execute(query)
query = "INSERT INTO web_command VALUES (null,'canva', 'https://www.canva.com/')"
cursor.execute(query)
conn.commit()
