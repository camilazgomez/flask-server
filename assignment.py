import psycopg2
import json
# important steps
# first we calculate number of components that each task has sorted by type on dict DONE
# second we check users ratios, for their level DONE
# if they have completed 0.5 of each ratio in their level they are upgraded to next level otherwise they stay in the same DONE
# if upgraded of level task is picked random on that category DONE
# if not upgraded task with most components on lowest category ratio is picked DONE
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
    facil = []
    medio = []
    dificil = []
    avanzado = []

    for task in tasks:
        diagram = task[5]

        if task[6] == "Facil":
            facil.append(task[0])
        if task[6] == "Medio":
            medio.append(task[0])
        if task[6] == "Dificil":
            dificil.append(task[0])
        if task[6] == "Avanzado":
            avanzado.append(task[0])

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
        new_task=new_task[0]

    else:
        temp = min(dict.values())
        res = [key for key in dict if dict[key] == temp][0]



        if student[4] == "Facil":
            if len(facil) > 1:
                ind = facil.index(int(student[3]))
                facil.pop(ind)

            new_task = facil[0]
            print(facil)


            for i in facil:
                if elements[i][res] > elements[new_task][res] or i != student[3]:
                    new_task = i

        elif student[4] == "Medio":
            print(medio)
            if len(medio) > 1:
                ind = medio.index(int(student[3]))
                medio.pop(ind)

            new_task = medio[0]

            for i in medio:
                if elements[i][res] > elements[new_task][res] or i != student[3]:
                    new_task = i

        elif student[4] == "Dificil":
            if len(dificil) > 1:
                ind = dificil.index(int(student[3]))
                dificil.pop(ind)

            new_task = dificil[0]
            print(dificil)


            for i in dificil:
                if elements[i][res] > elements[new_task][res] or i != student[3]:
                    new_task = i
        else:
            print(avanzado)
            if len(avanzado) > 1:
                ind = avanzado.index(int(student[3]))
                avanzado.pop(ind)

            new_task = avanzado[0]

            for i in avanzado:
                if elements[i][res] > elements[new_task][res] or i != student[3]:
                    new_task = i



        cur.execute(
            'UPDATE  student SET actual_task = %s WHERE email = %s',
            (new_task, mail,)
        )


    conn.commit()


    cur.close()
    conn.close()
    print("Nueva tarea:" + str(new_task))
    return new_task



