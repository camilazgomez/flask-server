import json

from flask import Flask, redirect, url_for, render_template, request, session
import psycopg2
import flask

host = "ec2-52-48-159-67.eu-west-1.compute.amazonaws.com"
database ="der0mspk63lkul"
user = "cxxhscojbmpoqh"
password = "128e61a28784fa578559358d2ff9653afceabf6728c39d91fa5419815f7616f2"

app = Flask(__name__)

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

        cur.execute('INSERT INTO tasks (title, professor, enunciado, level, diagram)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (todo_data["title"],
                     todo_data["professor"],
                     todo_data["enunciado"],
                     'Medio',
                     json.dumps(todo_data["diagram"])
                    ))

        conn.commit()

        cur.close()
        conn.close()
        return {"members": ["Member1", "Member2", "Member3"]}

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
            tasks_dict[element[0]]["data_added"] = element[7]

        conn.commit()

        cur.close()
        conn.close()

        return tasks_dict

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
               SET (enunciado, title,diagram) 
               = (%s, %s, %s)
            WHERE 
               id = %s""",
            [todo_data["enunciado"], todo_data["title"], json.dumps(todo_data["diagram"]), todo_data["id"]]
        )

        conn.commit()

        cur.close()
        conn.close()
        return {"response": "Updated"}



if __name__ == "__main__":
    app.run(debug=True)
