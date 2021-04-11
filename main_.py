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
    dat=""
    name_columnas = bd.Nombre_Columnas("usuarios")
    cli = bd.Consulta("usuarios")
    for i in range(len(name_columnas)):
        if i < len(name_columnas)-1:
            dat += format(name_columnas[i+1][0])

    return rt('Clientes.html', dat_colum=dat, Clientes=cli)

@app.route('/Cliente_Nuevo', methods=['POST'])
def client():
   
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Tipo_GPS = request.form['Tipo_GPS']
        numero_sim = request.form['Numero_Sim_GPS']
        pago_mensual = request.form['Pago_Mensual']
        Cedula = request.form['Cedula']
        estdo = request.form['Estado']
        ID = request.form['ID']
        fecha = request.form['Fecha_Afiliacion']
        marca = request.form['Marca_Vehiculo']
        Placa = request.form['PlacaV']
        color = request.form['Color']

        todo = [0,nombre,telefono,correo,numero_sim,
        Cedula,estdo,pago_mensual,fecha,Tipo_GPS,marca,
        Placa,color,ID]
        bd.Registrar(todo,'usuarios')
        return rt("Cliente_Nuevo.html")
    


if __name__ == '__main__':
    app.run(port = 3000,debug= True)