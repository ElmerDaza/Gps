from flask import Flask, render_template as rt, request, redirect, url_for
import BDsql as bd

app = Flask(__name__)

#configuracion
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    return rt('index.html')

@app.route('/Control')
def ControlPagina():
    return rt('Control.html')

@app.route('/Clientes')
def Clientes():
    dat=[]
    name_columnas = bd.Nombre_Columnas("usuarios")
    cli = bd.Consulta("usuarios")
    for i in range(len(name_columnas)):
        if i < len(name_columnas)-1:
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i+1][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return rt('Clientes.html', dat_colum=dat, Clientes=cli,contenido=sin_contenido)

@app.route('/Cliente_Nuevo', methods=['POST'])
def client_new():
   
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        clave=request.form['ID']
        fecha = request.form['Fecha_Afiliacion']
        

        todo = [0,nombre,telefono,correo,
        Cedula,clave,fecha]
        bd.Registrar(todo,'usuarios')
        return redirect("Clientes")
   

@app.route('/Eliminar/<string:id>')
def delete(id):

    print(id)
    bd.Consulta_elimina("usuarios", id)
    

    return redirect(url_for("Clientes"))

@app.route('/Editar/<id>')
def edit(id):
    respuesta = bd.Consultar_Usuario("usuarios",id)
    return rt("Editar_Cliente.html", dat=respuesta[0])

@app.route('/Modificar/<id>', methods=['POST'])
def Modificar(id):
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        Clave = request.form['ID']
        fecha = request.form['Fecha_Afiliacion']

        todo = [nombre, telefono, correo, Cedula,Clave,fecha]
        
        bd.Modificar_Usuario("usuarios",id,todo)
        return redirect(url_for("Clientes"))
        

@app.route('/Vehiculos')
def Vehiculos():
    dat=[]
    name_columnas = bd.Nombre_Columnas("vehiculos")
    cli = bd.Consulta("vehiculos")
    for i in range(len(name_columnas)):
        if i < len(name_columnas)-1:
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i+1][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return rt('Vehiculos.html', dat_colum=dat, vehiculos=cli,contenido=sin_contenido)

@app.route('/Vehiculo_Nuevo', methods=['POST'])
def vehicle_new():
   
    if request.method == 'POST':
        placa = request.form['placa']
        gps =  request.form['Modelo_GPS']
        sim =  request.form['Numero_simcard']
        vehiculo = request.form['Descripcion_Vehiculo']
        dueño=request.form['Dueño_Vehiculo']
        fecha = request.form['Fecha_Instalacion']
        imei= request.form['Imei']
        tipo = request.form['Tipo_Instalacion']

        todo = [0,placa,gps,sim,vehiculo,dueño,imei,tipo,fecha]
        bd.Registrar(todo,'vehiculos')
        return redirect("Vehiculos")

@app.route('/Editar_Vehiculo/<id>')
def EditVehicle(id):
    respuesta = bd.Consultar_Usuario("vehiculos",id)
    return rt("Editar_Vehiculo.html", dat=respuesta[0])

@app.route('/Modificar_Vehiculo/<id>', methods=['POST'])
def Modificar_Vehiculo(id):
    placa = request.form['placa']
    gps =  request.form['Modelo_GPS']
    sim =  request.form['Numero_simcard']
    vehiculo = request.form['Descripcion_Vehiculo']
    dueño=request.form['Dueño_Vehiculo']
    fecha = request.form['Fecha_Instalacion']
    imei= request.form['Imei']
    tipo = request.form['Tipo_Instalacion']
    todo = [0,placa,gps,sim,vehiculo,dueño,imei,tipo,fecha]
    bd.Modificar_Usuario("vehiculos",id,todo)
    return redirect(url_for("Vehiculos"))


if __name__ == '__main__':
    app.run(port = 3000,debug= True)