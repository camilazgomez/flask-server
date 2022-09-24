import psycopg2
import json
# important steps
# first we calculate number of components that each task has sorted by type on dict DONE
# second we check users ratios, for their level DONE
# if they have completed 0.5 of each ratio in their level they are upgraded to next level otherwise they stay in the same
# if upgraded of level task is picked random on that category
# if not upgraded task with most components on lowest category ratio is picked
host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"


def pick_task(mail):
    forward = {"Facil": "Medio", "Medio": "Dificil", "Dificil": "Avanzado", "Avanzado": "Avanzado"}
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)
    cur = conn.cursor()

    cur.execute('SELECT * from tasks')
    tasks = cur.fetchall()

    elements = {}
    for task in tasks:
        diagram = task[5]
        elements[task[0]]={}
        elements[task[0]]["fijo"] = len(diagram["apoyoFijo"])
        elements[task[0]]["deslizante"] = len(diagram["apoyoDeslizante"])
        elements[task[0]]["empotrado"] = len(diagram["empotrado"])
        elements[task[0]]["momento"] = len(diagram["momentums"])
        elements[task[0]]["fuerza"] = 0
        elements[task[0]]["angulo"] = 0
        blackarrows = diagram["blackarrow"]
        for f in blackarrows:
            if f["rotation"] in [0,90,-90,180,-180]:
                elements[task[0]]["fuerza"] += 1
            else:
                elements[task[0]]["angulo"] += 1

    print(elements)

    cur.execute('SELECT * FROM student WHERE email = %s',
                (mail,)
                )

    student = cur.fetchone()

    dict = {}

    # Estudiante nivel facil: fijo fuerza y deslizante
    if student[4]=="Facil":
        dict["fijo"] = student[6]
        dict["deslizante"] = student[7]
        dict["fuerza"] = student[11]
    # Estudiante nivel Medio: empotramiento momento
    elif student[4]=="Medio":
        dict["momento"] = student[10]
        dict["empotrado"] = student[8]
    # Estudiante nivel dificil: angulo
    elif student[4]=="Dificil":
        dict["angulo"] = student[12]
    # Estudiante nivel Avanzado: Vinculos internos rotula biela
    else:
        dict["rotula"] = student[5]
        dict["biela"] = student[9]

    next = all(value >= 0.5 for value in dict.values())

    print(dict)
    print ("condicion:" + str(next))
    if (next):
        cur.execute('SELECT * FROM tasks WHERE level = %s ',
                    (forward[student[4]],)
                    )
        new_task = cur.fetchone()

        cur.execute(
            'UPDATE  student SET (level, actual_task) = (%s, %s) WHERE email = %s',
            (forward[student[4]], new_task[0], mail)
        )

    conn.commit()


    cur.close()
    conn.close()


pick_task("prueba@gmail.com")
