import json

from flask import Flask, redirect, url_for, render_template, request, session
import psycopg2
import flask
from flask_cors import CORS
from assignment import *
from checkfirst import *
from checkthird import *
from updateStudent import *

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
        cur.execute('SELECT * FROM tasks WHERE level = %s ',
                    ("Facil",)
                    )

        task = cur.fetchone()[0]
        conn.commit()


        cur.execute('SELECT * FROM student WHERE email = %s ',
                    (todo_data["email"],)
                    )

        record = cur.fetchall()
        if len(record) == 0:
            cur.execute('INSERT INTO student (email, password,actual_task,level,rotula,fijo,deslizante,empotrado,biela,momento,fuerza,angulo,'
                        'rotula_total, fijo_total, deslizante_total, empotrado_total,biela_total, momento_total, fuerza_total,'
                        'angulo_total, rotula_unit, fijo_unit, deslizante_unit, empotrado_unit,biela_unit, momento_unit, fuerza_unit,'
                        'angulo_unit )'
                        'VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s)',
                        (todo_data["email"],
                         todo_data["password"],
                         task,
                         "Facil",
                         0.0,0.0, 0.0,0.0, 0.0,0.0,0.0, 0.0,
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

                         ))
            cur.execute('SELECT LASTVAL()')
            lastid = cur.fetchone()[0]

            cur.execute('INSERT INTO distribution (id_task, id_student, first_step, second_step, third_step, fourth_step)'
                        'VALUES (%s, %s, %s, %s,%s, %s)',
                        (task,lastid,None, True, None, None ))

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


@app.route("/task")
def task():
    mail = request.args.get('email')


    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE email = %s',
                (mail,)
                )

    task_id = cur.fetchone()[3]


    conn.commit()

    cur.execute('SELECT * FROM tasks WHERE id = %s',
                (task_id,)
                )

    task = cur.fetchone()


    tasks_dict = {}
    tasks_dict["id"] = task[0]
    tasks_dict["title"] = task[1]
    tasks_dict["professor"] = task[2]
    tasks_dict["enunciado"] = task[3]
    tasks_dict["picture"] = task[4]
    tasks_dict["diagram"] = task[5]
    tasks_dict["level"] = task[6]
    tasks_dict["data_added"] = task[9]
    tasks_dict["etapa"] = task[7]
    tasks_dict["etapafin"] = task[8]

    conn.commit()

    cur.close()
    conn.close()


    return tasks_dict

@app.route('/delete')
def delete():
    id_get = request.args.get('task')
    print(id_get)
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    '''
    cur.execute('SELECT * FROM tasks WHERE id= %s',
                (id_get,))

    task_level = cur.fetchone()[6]

    cur.execute('SELECT * FROM tasks WHERE level = %s and id != %s',
                (task_level,id_get))

    replacement = cur.fetchone()[0]

    cur.execute('UPDATE student SET actual_task = %s WHERE actual_task = %s' ,
                [replacement, id_get])
    '''
    cur.execute('DELETE FROM tasks WHERE id = %s',
                (id_get,)
                )

    conn.commit()

    cur.close()
    conn.close()

    return {'response': 'success'}

@app.route("/students")
def students():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()

    cur.execute('SELECT * FROM student '
                )
    students = cur.fetchall()
    dict = {}
    for student in students:
        dict[student[0]] = {}
        dict[student[0]]["id"] = student[0]
        dict[student[0]]["email"] = student[1]
        dict[student[0]]["actual_task"] = student[3]
        dict[student[0]]["level"] = student[4]
        dict[student[0]]["rotula"] = student[5]
        dict[student[0]]["fijo"] = student[6]
        dict[student[0]]["deslizante"] = student[7]
        dict[student[0]]["empotrado"] = student[8]
        dict[student[0]]["biela"] = student[9]
        dict[student[0]]["momento"] = student[10]
        dict[student[0]]["fuerza"] = student[11]
        dict[student[0]]["angulo"] = student[12]
        dict[student[0]]["date_added"] = student[13]



    conn.commit()

    cur.close()
    conn.close()

    return dict


@app.route("/student")
def student():
    id_get = request.args.get('email')
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()

    cur.execute('SELECT * FROM student WHERE email = %s ',
                (id_get,)
                )
    student = cur.fetchone()
    dict = {}

    dict["id"] = student[0]
    dict["email"] = student[1]
    dict["actual_task"] = student[3]
    dict["level"] = student[4]
    dict["rotula"] = student[5]
    dict["fijo"] = student[6]
    dict["deslizante"] = student[7]
    dict["empotrado"] = student[8]
    dict["biela"] = student[9]
    dict["momento"] = student[10]
    dict["fuerza"] = student[11]
    dict["angulo"] = student[12]
    dict["date_added"] = student[13]



    conn.commit()

    cur.close()
    conn.close()

    return dict

@app.route("/next_task")
def next_task():
    email_get = request.args.get('email')


    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE email = %s',
                (email_get,))
    student = cur.fetchone()
    id_get = student[0]
    old_task = student[3]

    updateStudent(str(old_task), str(id_get))
    new_task = pick_task(email_get)
    task_id = new_task
    print(new_task)



    cur.execute('INSERT INTO distribution (Id_task, Id_student, first_step, second_step, third_step, fourth_step)'
                'VALUES (%s, %s, %s, %s,%s, %s)',
                (int(task_id), int(id_get), None, True, None, None))


    conn.commit()

    cur.execute('SELECT * FROM tasks WHERE id = %s',
                (task_id,)
                )

    task = cur.fetchone()

    tasks_dict = {}
    tasks_dict["id"] = task[0]
    tasks_dict["title"] = task[1]
    tasks_dict["professor"] = task[2]
    tasks_dict["enunciado"] = task[3]
    tasks_dict["picture"] = task[4]
    tasks_dict["diagram"] = task[5]
    tasks_dict["level"] = task[6]
    tasks_dict["data_added"] = task[9]
    tasks_dict["etapa"] = task[7]
    tasks_dict["etapafin"] = task[8]

    conn.commit()

    cur.close()
    conn.close()
    return tasks_dict

@app.route("/checkone",  methods= ['POST'])
def checkone():
    todo_data = request.get_json()
    response = check_first(todo_data["id_task"], todo_data["diagram"], todo_data["punto"])

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE email = %s',
                (todo_data["email"],))
    id_get = cur.fetchone()[0]

    if response[0] == True:
        cur.execute('UPDATE distribution SET first_step = %s WHERE id_task = %s and id_student = %s',
           [ True, todo_data["id_task"], id_get])
        conn.commit()
        return {"response": "true", "nuevoPunto": response[1]}

    cur.execute('UPDATE distribution SET first_step = %s WHERE id_task = %s and id_student = %s',
                [False, todo_data["id_task"], id_get])


    conn.commit()

    cur.close()
    conn.close()


    return {"response": json.dumps(response[0]), "nuevoPunto": response[1]}


@app.route("/checkthird",  methods= ['POST'])
def checkthird():
    todo_data = request.get_json()
    response = check_third(todo_data["id_task"], todo_data["diagram"])

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE email = %s',
                (todo_data["email"],))
    id_get = cur.fetchone()[0]


   #actualizar distribucion copy paste del otro

    if response[0] == True:
        cur.execute('UPDATE distribution SET third_step = %s WHERE id_task = %s and id_student = %s',
           [ True, todo_data["id_task"], id_get])
        conn.commit()
        return {"response": "true", "nuevoPunto": response[1]}

    cur.execute('UPDATE distribution SET third_step = %s WHERE id_task = %s and id_student = %s',
                [False, todo_data["id_task"], id_get])


    conn.commit()

    cur.close()
    conn.close()

    if response[0] == True:
        {"response": response[0]}


    return {"response": response[1] }


@app.route("/check4",  methods= ['POST'])
def check_fourth():
    todo_data = request.get_json()
    response = todo_data["response"]

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE email = %s',
                (todo_data["email"],))
    id_get = cur.fetchone()[0]

    if response == True:
        cur.execute('UPDATE distribution SET fourth_step = %s WHERE id_task = %s and id_student = %s',
                    [True, todo_data["id_task"], id_get])
        conn.commit()
        cur.close()
        conn.close()
        return {"response": "succes"}

    cur.execute('UPDATE distribution SET fourth_step = %s WHERE id_task = %s and id_student = %s',
                [False, todo_data["id_task"], id_get])
    conn.commit()
    cur.close()
    conn.close()
    return {"response": "succes"}




if __name__ == "__main__":
    app.run(debug=True)
