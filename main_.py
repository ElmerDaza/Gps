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

if __name__ == '__main__':
    app.run(port = 3000,debug= True)