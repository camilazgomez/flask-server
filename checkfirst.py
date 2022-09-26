import psycopg2
import json


host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"

def check_first (id, diagram, punto):
    punto = chr(punto)
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cur = conn.cursor()

    cur.execute('SELECT * FROM tasks WHERE id = %s',
                (id,))

    task = cur.fetchone()

    og_diagram = task[5]

    new_punto = "A"
    marks = {}
    marks["apoyoDeslizante"]={}
    for element in og_diagram["apoyoDeslizante"]:
        marks["apoyoDeslizante"][element["id"]] = {"found" : False, "id":None, "punto": element["unionid"]}

    marks["apoyoFijo"] = {}
    for element in og_diagram["apoyoFijo"]:
        marks["apoyoFijo"][element["id"]] = {"found" : False, "id":None, "punto": element["unionid"]}

    marks["empotrado"] = {}
    for element in og_diagram["empotrado"]:
        marks["empotrado"][element["id"]] = {"found" : False, "id":None, "punto": element["unionid"]}

    marks["blackarrow"] = {}
    for element in og_diagram["blackarrow"]:
        marks["blackarrow"][element["id"]] = {"found" : False, "id":None}

    marks["biela"] = {}
    for element in og_diagram["biela"]:
        marks["biela"][element["id"]] = {"found" : False, "id":None}

    marks["momentums"] = {}
    for element in og_diagram["momentums"]:
        marks["momentums"][element["id"]] = {"found" : False, "id":None}

    marks["rectangles"] = {}
    for element in og_diagram["rectangles"]:
        marks["rectangles"][element["id"]] = {"found" : False, "id":None}

    # chequear si estan todos los elmentos correctos DONE
    quantities = True
    feedback = []
    if len(og_diagram["apoyoDeslizante"]) != len(diagram["apoyoDeslizante"]):
        quantities = False
        if len(og_diagram["apoyoDeslizante"]) > len(diagram["apoyoDeslizante"]):
            feedback.append("Faltan apoyos deslizantes")
        else:
            feedback.append("Sobran apoyos deslizantes")

    if len(og_diagram["apoyoFijo"]) != len(diagram["apoyoFijo"]):
        quantities = False
        if len(og_diagram["apoyoFijo"]) > len(diagram["apoyoFijo"]):
            feedback.append("Faltan apoyos fijos")
        else:
            feedback.append("Sobran apoyos fijos")

    if len(og_diagram["empotrado"]) != len(diagram["empotrado"]):
        quantities = False
        if len(og_diagram["empotrado"]) > len(diagram["empotrado"]):
            feedback.append("Faltan empotrados")
        else:
            feedback.append("Sobran empotrados")

    if len(og_diagram["blackarrow"]) != len(diagram["blackarrow"]):
        quantities = False
        if len(og_diagram["blackarrow"]) > len(diagram["blackarrow"]):
            feedback.append("Faltan fuerzas puntuales")
        else:
            feedback.append("Sobran fuerzas puntuales")

    if len(og_diagram["momentums"]) != len(diagram["momentums"]):
        quantities = False
        if len(og_diagram["momentums"]) > len(diagram["momentums"]):
            feedback.append("Faltan momentumss")
        else:
            feedback.append("Sobran momentums")

    if len(og_diagram["rectangles"]) != len(diagram["rectangles"]):
        quantities = False
        if len(og_diagram["rectangles"]) > len(diagram["rectangles"]):
            feedback.append("Faltan barras")
        else:
            feedback.append("Sobran barras")

    if quantities == False:
        print(feedback)
        return feedback, new_punto

    dog = matriz_distancias(og_diagram)
    nog = matriz_distancias(diagram)

    # chequear si elementos estan en posición correcta DONE
    for d in dog[0]:
        count =0
        for n in nog[0]:
            copyd = d[:]
            copyn = n[:]
            copyd.sort()
            copyn.sort()
            subtracted = list()
            for item1, item2 in zip(copyd, copyn):
                item = item1 - item2
                subtracted.append(item)
            print("**********")
            print(subtracted)
            print("**********")
            if sum(subtracted)<= 30 and sum(subtracted)>= -30  and dog[1][count][0]==nog[1][count][0]:
                marks[dog[1][count][0]][dog[1][count][1]]["found"] = True
                marks[dog[1][count][0]][dog[1][count][1]]["id"] = nog[1][count][1]
            count+=1

    # Encontrar nuevo punto de momento
    id_newp =""

    for element in marks:
        if element in ["apoyoDeslizante", "apoyoFijo", "empotrado"]:
            for i in marks[element]:
                print(marks[element][i])
                if marks[element][i]["punto"] == punto:
                    id_newp = marks[element][i]["id"]
    print("***************")
    print(id_newp)
    print("***************")

    apoyos = ["apoyoDeslizante", "apoyoFijo", "empotrado"]
    for tipo in apoyos:
        for elemento in diagram[tipo]:
            if elemento["id"] == id_newp:
                new_punto = elemento["unionid"]
    print("Nuevo Punto: " + new_punto)


    feedback = []
    print(marks)

    for elemento in marks:
        for item in marks[elemento]:
            print(item)
            if marks[elemento][item]["found"] == False:
                if elemento == "rectangles":
                    feedback.append("Barra mal ubicada")
                elif elemento == "momentums":
                    feedback.append("Momento mal ubicada")
                else:
                    feedback.append(elemento + " mal ubicado")
    if len(feedback) > 0:
        print(feedback)
        return feedback, new_punto




    feedback = []
    magnitudes = True
    angulos = True
    # chequear magnitudes
    tipos = ["blackarrow", "momentums"]
    for tipo in tipos:
        for elemento in marks[tipo]:

            if og_diagram["inputs"][elemento] != diagram["inputs"][marks[tipo][elemento]["id"]]:
                magnitudes = False
                if tipo == "blackarrow":
                    feedback.append("Revisa Magnitud de la fuerza de "+ str(diagram["inputs"][marks[tipo][elemento]["id"]])+ "N")
                else:
                    feedback.append(
                        "Revisa Magnitud del momento con " + str(diagram["inputs"][marks[tipo][elemento]["id"]]) + "Nm")

    # chequear angulos
    for tipo in tipos:
        for elemento in og_diagram[tipo]:
            for aux in diagram[tipo]:
                if aux["id"] == elemento["id"]:
                    if (aux["rotation"] - elemento["rotation"]) >1 or (aux["rotation"] - elemento["rotation"])<-1 :
                        angulos = False
                        feedback.append("Corregir una fuerza con ángulo "+ str(aux["rotation"])+"º")


    if magnitudes == False or angulos == False:
        print(feedback)
        return feedback, new_punto


    print(marks)

    conn.commit()


    cur.close()
    conn.close()
    return True,  new_punto


def matriz_distancias (diagram):
    tipos = ["apoyoDeslizante", "apoyoFijo", "empotrado", "blackarrow", "biela", "circles", "momentums","rectangles"]
    matrix = []
    orden =[]

    for tipo in tipos:
        for element in diagram[tipo]:
            dis = []
            orden.append((tipo,element["id"]))
            for tip in tipos:
                for i in diagram[tip]:
                    distancia = ((element["y"]-i["y"])**2+(element["x"]-i["x"])**2)**(1/2)
                    dis.append(round(distancia,2))
            matrix.append(dis)




    return matrix, orden







