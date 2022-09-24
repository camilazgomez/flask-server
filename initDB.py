import os
import psycopg2

host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS tasks;')

cur.execute('CREATE TABLE tasks (id serial PRIMARY KEY,'
            'title varchar (150) NOT NULL,'
            'professor varchar (150) NOT NULL,'
            'enunciado varchar (1000) NOT NULL,'
            'picture bytea,'
            'diagram json,'
             'level varchar (150) ,'
            'step varchar (150) ,'
            'end_step varchar (150) ,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table



conn.commit()

cur.close()
conn.close()
