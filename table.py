import sqlite3

connection = sqlite3.connect('database.db')

# query = ' create table comments(text varchar(8000))'
query2 = 'delete from comments'

cursor = connection.cursor()
cursor.execute(query2)
connection.commit()

connection.close()