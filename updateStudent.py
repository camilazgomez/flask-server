import psycopg2
import json


host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"


def updateStudent(id_task, id_student):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()

    cur.execute('SELECT * FROM tasks WHERE id = %s',
                (id_task,)
                )
    task = cur.fetchone()
    diagram = task[5]

    cur.execute('SELECT * FROM student WHERE id = %s',
                (id_student,)
                )

    '''
    student = cur.fetchone()[0]
    rotula = student['rotula']
    fijo = student['fijo']
    deslizante = student['deslizante']
    empotrado = student['empotrado,']
    biela = student['biela']
    momento =student['momento']
    fuerza = student['fuerza']
    angulo = student['angulo']
    rotula_total = student['rotula_total']
    fijo_total = student['fijo_total']
    deslizante_total = student['deslizante_total']
    empotrado_total = student['empotrado_total']
    biela_total = student['biela_total']
    momento_total = student['momento_total']
    fuerza_total = student['fuerza_total']
    student['angulo_total']
    student['rotula_unit']
    student['fijo_unit']
    student['deslizante_unit']
    student['empotrado_unit']
    student['biela_unit']
    student['momento_unit']
    student['fuerza_unit']
    student['angulo_unit']
    '''


    cur.execute('SELECT * FROM distribution WHERE id_student = %s and id_task = %s ',
                (id_student,id_task)
                )

    distribution = cur.fetchone()
    trues = 1
    for i in range(3,7):
        if distribution[i] == True:
            trues+=1


    for element in diagram:
        if element == "apoyoDeslizante" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET deslizante_unit = deslizante_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET deslizante_total = deslizante_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET deslizante = CAST(deslizante_unit AS float)/CAST(deslizante_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "apoyoFijo" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET fijo_unit = fijo_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET fijo_total = fijo_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET fijo = CAST(fijo_unit AS float)/CAST(fijo_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "empotrado" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET empotrado_unit = empotrado_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET empotrado_total = empotrado_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET empotrado = CAST(empotrado_unit AS float)/CAST(empotrado_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "circles" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET rotula_unit = rotula_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET rotula_total = rotula_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET rotula = CAST(rotula_unit AS float)/CAST(rotula_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "biela" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET biela_unit = biela_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET biela_total = biela_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET biela = CAST(biela_unit AS float)/CAST (biela_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "momentums" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET momento_unit = momento_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET momento_total = momento_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET momento = CAST(momento_unit AS float)/CAST(momento_total AS float) WHERE id = %s',
                        (id_student,))
        elif element == "blackarrow" and len(diagram[element])>=1:
            if trues >= 2:
                cur.execute('UPDATE student SET fuerza_unit = fuerza_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET fuerza_total = fuerza_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET fuerza = CAST(fuerza_unit AS float)/CAST(fuerza_total AS float) WHERE id = %s',
                        (id_student,))
            if trues >= 2:
                cur.execute('UPDATE student SET angulo_unit = angulo_unit+1 WHERE id = %s',
                            (id_student,))
            cur.execute('UPDATE student SET angulo_total = angulo_total+1 WHERE id = %s',
                        (id_student,))
            cur.execute('UPDATE student SET angulo = CAST(angulo_unit AS float)/CAST(angulo_total AS float) WHERE id = %s',
                        (id_student,))



    conn.commit()


    cur.close()
    conn.close()

