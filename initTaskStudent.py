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
cur.execute('DROP TABLE IF EXISTS distribution;')

cur.execute('CREATE TABLE distribution (id serial PRIMARY KEY,'
            'id_student integer,'
            'id_task integer,'
            'first_step bool,'
            'second_step bool,'
            'third_step bool,'
            'fourth_step bool,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table



conn.commit()

cur.close()
conn.close()
