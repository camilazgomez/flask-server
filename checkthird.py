import psycopg2
import json



host = "ec2-52-210-97-223.eu-west-1.compute.amazonaws.com"
database ="dfsdqhnrnbpm5g"
user = "kthnlujwvbiowt"
password = "0ca18ed348950aab5d8be053aca64603ba6c344ae48dfc9eefd8b5f006039ad1"


def check_third( id, diagram):
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

    apoyos = ["apoyoDeslizante", "apoyoFijo",  "empotrado"]
    incognitas = ["incognitaf", "momentumi"]

    counter_fo = 0
    counter_mo = 0
    for tipo in apoyos:
        for item in og_diagram[tipo]:
            if tipo == "apoyoDeslizante":
                counter_fo+=1
            else:
                counter_fo+=2
                if tipo == "empotrado":
                    counter_mo +=1
    feedback =[]


    for tipo in incognitas:
        if tipo == "incognitaf":
            if len(diagram[tipo]) > counter_fo:
                feedback.append("Sobra "+str((len(diagram[tipo]) - counter_fo))+" fuerzas de reacción")
            elif len(diagram[tipo]) < counter_fo:
                feedback.append("Falta "+ str((counter_fo - len(diagram[tipo])))+" fuerzas de reacción")
        if tipo == "momentumi":
            if len(diagram[tipo]) > counter_mo:
                feedback.append("Sobra "+str((len(diagram[tipo]) - counter_mo))+" momentos reacción")
            elif len(diagram[tipo]) < counter_mo:
                feedback.append("Falta"+str((counter_mo - len(diagram[tipo])))+" momentos reacción")

    if len(feedback)>0:
        return False, feedback

    marks = {}
    for tipo in apoyos:
        marks[tipo]= {}
        for item in og_diagram[tipo]:
            close = closest(item["x"], item["y"], og_diagram["rectangles"])
            if tipo == "apoyoDeslizante":
                marks[tipo][item["id"]] = {"H": False, "x": item["x"], "y":  item["y"],"rotation": item["rotation"],
                                           "closer": close}
            elif tipo == "apoyoFijo":
                marks[tipo][item["id"]] = {"H": False,"V": False, "x": item["x"], "y":  item["y"],
                                           "rotation": item["rotation"],
                                           "closer": close}
            else:
                marks[tipo][item["id"]] = {"H": False, "V": False,"M": False, "x": item["x"], "y": item["y"],
                                           "rotation": item["rotation"],
                                           "closer": close}

    for elemento in diagram["incognitaf"]:
        distancia = closest(elemento["x"], elemento["y"], diagram["rectangles"])
        for tipo in marks:
            for item in marks[tipo]:


                if (marks[tipo][item]["closer"]-distancia < 50 and marks[tipo][item]["closer"]-distancia > -50 and \
                        (elemento["rotation"] == 0 or elemento["rotation"] == 180\
                         or elemento["rotation"]==-180)):
                    marks[tipo][item]["H"] = True
                if (marks[tipo][item]["closer"]-distancia < 200 and marks[tipo][item]["closer"]-distancia > -200 and \
                        ((elemento["rotation"]**2)**(1/2)-90<1 and (elemento["rotation"]**2)**(1/2)-90>-1)):
                    marks[tipo][item]["V"] = True

    for elemento in diagram["momentumi"]:
        distancia = closest(elemento["x"], elemento["y"], diagram["rectangles"])
        for item in marks["empotrado"]:
            if (marks["empotrado"][item]["closer"]-distancia <50 and marks["empotrado"][item]["closer"]-distancia >50):
                marks[tipo][item]["M"] = True

    feedback = []
    dh= 0
    fh=0
    fv=0
    em=0
    eh=0
    ev=0
    for elemento in marks:
        for item in marks[elemento]:
            if elemento == "apoyoDeslizante":
                if marks[elemento][item]["H"]== False:
                    dh+=1
            elif elemento == "apoyoFijo":
                if marks[elemento][item]["V"] == False:
                    fv+=1
                if marks[elemento][item]["H"] == False:
                    fh+=1
            else:
                if marks[elemento][item]["V"] == False:
                    ev+=1
                if marks[elemento][item]["H"] == False:
                    eh+=1
                if marks[elemento][item]["M"] == False:
                    em+=1


    if dh >0:
        feedback.append("Falta "+ str(dh)+" fuerza de reacción horizontal perteneciente a apoyo deslizante")
    if fh > 0:
        feedback.append("Falta " + str(fh) + " fuerza de reacción horizontal perteneciente a apoyo fijo")
    if fv > 0:
        feedback.append("Falta " + str(fv) + " fuerza de reacción vertical perteneciente a apoyo fijo")
    if eh > 0:
        feedback.append("Falta " + str(eh) + " fuerza de reacción horizontal perteneciente a  empotrado")
    if ev > 0:
        feedback.append("Falta " + str(ev) + " fuerza de reacción vertical perteneciente a empotrado")
    if em > 0:
        feedback.append("Falta " + str(em) + " momento de reacción perteneciente a  empotrado")

    print(marks)
    print(feedback)

    if len(feedback)>0:
        return False, feedback

    print(marks)
    print(feedback)
    return True, feedback

def closest (x,y,rectangles):
    min = 10000000000000000
    for bar in rectangles:
        distancia = ((x-bar["x"])**2+(y-bar["y"]))**(1/2)
        if distancia < min:
            min = distancia
    return min






