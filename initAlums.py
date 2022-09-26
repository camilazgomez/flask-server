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
cur.execute('DROP TABLE IF EXISTS student;')

cur.execute('CREATE TABLE student (id serial PRIMARY KEY,'
            'email varchar (150) ,'
            'password varchar (150) ,'
            'actual_task varchar (1000) ,'
            'level varchar (150) ,'
            'rotula float ,'
            'fijo float ,'
            'deslizante float ,'
            'empotrado float ,'
            'biela float ,'
            'momento float ,'
            'fuerza float ,'
            'angulo float ,'
            'rotula_total integer ,'
            'fijo_total integer ,'
            'deslizante_total integer ,'
            'empotrado_total integer ,'
            'biela_total integer ,'
            'momento_total integer ,'
            'fuerza_total integer ,'
            'angulo_total integer ,'
            'rotula_unit integer ,'
            'fijo_unit integer ,'
            'deslizante_unit integer ,'
            'empotrado_unit integer ,'
            'biela_unit integer ,'
            'momento_unit integer ,'
            'fuerza_unit integer ,'
            'angulo_unit integer ,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )




conn.commit()

cur.close()
conn.close()
