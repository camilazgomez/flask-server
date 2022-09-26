import psycopg2
import json


host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"



conn = psycopg2.connect(
host=host,
database=database,
user=user,
password=password)

cur = conn.cursor()
cur.execute('INSERT INTO distribution (Id_task, Id_student, first_step, second_step, third_step, fourth_step)'
                'VALUES (%s, %s, %s, %s,%s, %s)',
                (2, 3, None, True, None, True))

conn.commit()

cur.close()
conn.close()
