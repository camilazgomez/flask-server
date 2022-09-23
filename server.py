import json

from flask import Flask, redirect, url_for, render_template, request, session
import psycopg2
import flask
from flask_cors import CORS

host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"

app = Flask(__name__)
CORS(app)

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/tasks", methods= ['POST', 'GET'])
def tasks():
    if flask.request.method == "POST":
        todo_data = request.get_json()
        print(todo_data)
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        cur = conn.cursor()

        cur.execute('INSERT INTO tasks (title, professor, enunciado, level, diagram, step, end_step)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (todo_data["title"],
                     todo_data["professor"],
                     todo_data["enunciado"],
                     todo_data["level"],
                     json.dumps(todo_data["diagram"]),
                     todo_data["etapa"],
                     todo_data["end_step"],

                    ))

        cur.execute('SELECT LASTVAL()')
        id_of_new_row = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        response = flask.jsonify({'response': 'success', 'id': id_of_new_row})


        return response

    if flask.request.method == "GET":
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        cur = conn.cursor()

        cur.execute('SELECT * FROM tasks')
        tasks = cur.fetchall()
        tasks_dict ={}
        print(tasks)
        for element in tasks:
            tasks_dict[element[0]] = {}
            tasks_dict[element[0]]["id"] = element[0]
            tasks_dict[element[0]]["title"] = element[1]
            tasks_dict[element[0]]["professor"] = element[2]
            tasks_dict[element[0]]["enunciado"] = element[3]
            tasks_dict[element[0]]["picture"] = element[4]
            tasks_dict[element[0]]["diagram"] = element[5]
            tasks_dict[element[0]]["level"] = element[6]
            tasks_dict[element[0]]["data_added"] = element[9]
            tasks_dict[element[0]]["etapa"] = element[7]
            tasks_dict[element[0]]["etapafin"] = element[8]

        response = tasks_dict


        conn.commit()

        cur.close()
        conn.close()

        return response

@app.route("/update", methods= ['POST'])
def update():
    if flask.request.method == "POST":
        todo_data = request.get_json()
        print(todo_data)
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        cur = conn.cursor()

        cur.execute(
            """UPDATE 
                  tasks 
               SET (enunciado, title,diagram, level) 
               = (%s, %s, %s, %s)
            WHERE 
               id = %s""",
            [todo_data["enunciado"], todo_data["title"], json.dumps(todo_data["diagram"]), todo_data["level"], todo_data["id"]]
        )

        conn.commit()

        cur.close()
        conn.close()

        return {"response": "Updated"}


@app.route("/login", methods= ['POST'])
def login():
    if flask.request.method == "POST":
        todo_data = request.get_json()
        print(todo_data)
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)

        cur = conn.cursor()

        cur.execute('SELECT * FROM student WHERE email = %s ',
                    (todo_data["email"],)
                    )

        record = cur.fetchall()
        if len(record) == 0:
            cur.execute('INSERT INTO student (email, password,actual_task,level,rotula,fijo,deslizante,empotrado,biela,momento,fuerza,angulo)'
                        'VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)',
                        (todo_data["email"],
                         todo_data["password"],
                         None,
                         "Facil",
                         0.0,0.0, 0.0,0.0, 0.0,0.0,0.0, 0.0

                         ))

            response = flask.jsonify({'response': 'success', 'id': "new"})
            conn.commit()

            cur.close()
            conn.close()


            return response

        conn.commit()

        cur.close()
        conn.close()

        response = flask.jsonify({'response': 'success', 'id': "old"})


        return response





if __name__ == "__main__":
    app.run(debug=True)
