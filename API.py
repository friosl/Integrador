from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import operator
app= Flask(__name__)
CORS(app)
tipo_medicion={'sensor': 'FC28','variable':'Humedad de la tierra','unidades':'% vapor agua por metro cúbico'}

mediciones = [
    {'fecha': '2019-08-10 12:00:00', **tipo_medicion,'valor':5},
    {'fecha': '2018-02-10 02:00:00', **tipo_medicion,'valor':6},
    {'fecha': '2018-02-10 02:00:00', **tipo_medicion,'valor':8},
    {'fecha': '2018-02-10 02:00:00', **tipo_medicion,'valor':8},
    {'fecha': '2019-08-11 12:00:00', **tipo_medicion,'valor':9}
] 

mayoresFecha   = [{}]
mayoresValores = [{}]
def ordenar(): #Método burbuja.
    global mediciones
    for i in range(len(mediciones)-1,0,-1):
        for j in range(i):
            if mediciones[j].get('fecha') > mediciones[j+1].get('fecha'):
                temp = mediciones[j].get('fecha')
                mediciones[j].update({'fecha':mediciones[j+1].get('fecha')})
                mediciones[j+1].update({'fecha':temp})



@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones',methods=['GET'])
def getAll():
    # mediciones= sorted(datetime.strptime(mediciones['fecha'],'%Y-%m-%d %H:%M:%S').iterable(),key=operator.itemgetter(1),reverse=False)
    ordenar()
    return jsonify(mediciones)  

# Lo que hay qué hacer: POST,GETALL,GET (que nos haya tocado) 
#Hacer un sort en la lista de diccionarios para mostrarlo (por la originalidad xd)
@app.route('/mediciones/getMayoresA/<string:fecha>',methods=['GET']) #importante poner qué tipo de método será
def getMayoresA(fecha):
    mayoresFecha.clear()   #Evitar que se añadan los mismos datos
    mayoresValores.clear() #Evitar que se añadan los mismos datos
    Existe= False
    entrada=None
    if (len(fecha)<=3 and len(fecha)>0):
        for medicion in mediciones:
            x= medicion
            medicion = x['valor']
            valor = int(fecha)
            if (medicion>valor):
                Existe= True
                mayoresValores.append(x)
        return jsonify(mayoresValores) if Existe else 'No hay coincidencias'

    else:
        for medicion in mediciones:
            x=medicion
            medicion = datetime.strptime(x['fecha'],'%Y-%m-%d %H:%M:%S') #Conversión de dict a datetime.
            entrada = datetime.strptime(fecha,'%Y-%m-%d %H:%M:%S')
            if(medicion > entrada):
                Existe=True
                mayoresFecha.append(x)
        return jsonify(mayoresFecha) if Existe else 'No hay coincidencias'
# Para encontrar los mayores a cierta fecha o valor se debe invocar de esta manera usando el método GET:
#http://127.0.0.1:4080/mediciones/getMayoresA/7 -> para valores
#http://127.0.0.1:4080/mediciones/getMayoresA/<fecha> -> para fechas

@app.route('/mediciones',methods=['POST']) 
def postOne():
    now= datetime.now()
    body=request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S') 
    mediciones.append({**body,**tipo_medicion})
    return jsonify(mediciones)

# Para eliminar un registro se debe poner la fecha en que se hizo. Con método POST
# Con el link http://127.0.0.1:4080/mediciones/<fecha>

@app.route('/mediciones/<string:fecha>',methods=['DELETE']) #importante poner qué tipo de método será
def deleteOne(fecha):
    x = False
    for medicion in mediciones:
        if(fecha in medicion['fecha']):
            x = True
            mediciones.remove(medicion)
    return 'Eliminado' if x else 'No encontrado'
# Para eliminar un registro se debe poner la fecha en que se hizo. Con método DELETE
# Con el link http://127.0.0.1:4080/mediciones/<fecha>

@app.route('/mediciones/<string:fecha>',methods=['PUT'])
def putOne(fecha):
    body=request.json
    x=False
    for medicion in mediciones:
        if(fecha in medicion['fecha']):
                x = True
                medicion ['valor'] = body['valor']
    return 'Modificado' if x else 'No encontrado'
#Para modificar un valor, se pone la ruta http://127.0.0.1:4080/mediciones/<fecha> con método PUT
    #Donde fecha es la fecha que se quiere cambiar, y el valor se pone de tipo JSON en body de POSTMAN. De esta manera: {"valor:"número}

@app.route('/mediciones/cambiarTodos/<string:valor>',methods=['PUT'])
def cambiarValores(valor):
    valores=valor.split(',')
    v1=int(valores[0])
    v2=int(valores[1])
    if v2 > 100 or v2 < 0:
        return "número inválido"
    for medicion in mediciones:
        if(v1 == medicion['valor']):
            medicion ['valor']=v2
    return "Método cambiarTodos"

@app.route('/mediciones/deleteAll',methods=['DELETE'])
def deleteAll():
    global mediciones,mayoresFecha,mayoresValor
    mediciones.clear()
    mayoresFecha.clear()
    mayoresValores.clear()
    return "Datos eliminados"
#Se debe poner el link de esta manera: Usando el método PUT
    #http://127.0.0.1:4080/mediciones/cambiarTodos/num,num 
    # el primer número significa el valor a cambiar y el segundo, el valor por el que se va a cambiar.

app.run(port=4080,debug=True)
