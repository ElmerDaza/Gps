
#from msilib.schema import Error
import traceback
from flask import __version__
import os
from gps3 import gps3
import json
from flask import Flask, render_template as rt, request, redirect, url_for
import BDsql as bd
import BOT_WA as BW
from source import ClaseRecursos as cr,Recursos_main_ as rm
from sourse import ClasePDF as P
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#configuracion
app.secret_key = os.getenv('flask_secretkey')


@app.route('/')
def Index():
    return rt('index.html')

@app.route('/location')
def location():
    # Obtiene el número IMEI del dispositivo GPS desde la solicitud
    imei = request.args.get('imei')
    # Conecta al dispositivo GPS y obtiene la posición actual
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            # Si el número IMEI del dispositivo GPS es el esperado, guarda las coordenadas y sale del bucle
            if data_stream.TPV['imei'] == imei:
                lat = data_stream.TPV['lat']
                lon = data_stream.TPV['lon']
                break
    # Muestra la ubicación actual en un mapa utilizando Google Maps
    return rt('location.html', lat=lat, lon=lon)


@app.route('/Control')
def ControlPagina():
    return rt('Control.html')

@app.route('/Clientes')
def Clientes():
    dat,cli,sin_contenido=rm.Clientes()
    return rt('Clientes.html', dat_colum=dat, Clientes=cli,contenido=sin_contenido)

@app.route('/Cliente_Nuevo', methods=['POST'])
def client_new():
    rm.Cliente_Nuevo(request)
    return redirect("Clientes")
   

@app.route('/Eliminar/<string:id>')
def delete(id):
    bd.Consulta_elimina("usuarios", id)
    return redirect(url_for("Clientes"))

@app.route('/Eliminar_vehiculo/<string:id>')
def delete_(id):
    #print('se elimino el vehiculo de placa',id)
    bd.Consulta_elimina("vehiculos", id)
    return redirect(url_for("Vehiculos"))


@app.route('/Editar/<id>')
def edit(id):
    respuesta = bd.Consultar_Usuario("usuarios",id)
    return rt("Editar_Cliente.html", dat=respuesta[0])

@app.route('/Modificar/<id>', methods=['POST'])
def Modificar(id):
    rm.Modificar(request,id)
    return redirect(url_for("Clientes"))
        

@app.route('/Vehiculos')
def Vehiculos():
    dat, cli, sin_contenido,usuarios=rm.Vehiculos()

    return rt('Vehiculos.html', 
            dat_colum=dat, 
            vehiculos=cli,
            contenido=sin_contenido,
            datos=usuarios)

@app.route('/Vehiculo_Nuevo', methods=['POST'])
def vehicle_new():
    respuesta,placa=rm.Vehiculo_Nuevo(request,BW.valor_mes,BW.eb.day.year)
    if respuesta==True:
        return redirect("Vehiculos")
    else:
        return rt('Dato_Duplicado.html',
                    clave=placa,
                    anterior='/Vehiculos')

@app.route('/Editar_Vehiculo/<id>')
def EditVehicle(id):
    respuesta,clients,usercode=rm.Editar_Vehiculo(id)
    return rt("Editar_Vehiculo.html", 
                dat=respuesta[0],
                clientes=clients,
                usercode=usercode)

@app.route('/Modificar_Vehiculo/<id>', methods=['POST'])
def Modificar_Vehiculo(id):
    rm.Modificar_Vehiculo(request,id)
    return redirect(url_for("Vehiculos"))

@app.route('/Gestor_Cobros')
def Gestor_Cobros():
    return rt('Gestor_Cobros.html')

@app.route('/Cobranza/<var>', methods=['POST'])
def cobranza(var):
    respuesta,retorno,contenido_no_cobro,error=rm.Cobranza(request,var)
    if respuesta == True:
        rt(retorno,no_cobro=contenido_no_cobro,err=error)
        
    else:
        return rt(retorno,err=error)



@app.route('/Informacion_Rapida')
def Informacion_Rapida():
    return rt('Informacion_Rapida.html')


@app.route('/Crear_Factura')
def Crear_factura():
    dat=bd.Consulta('usuarios')
    product=bd.Consulta('productos')
    return rt('CrearFactura.html',datos=dat,product=product)

@app.route('/FacturaEgreso')
def egr():
    u=bd.Ultimo_Registro('caja','codigo_caja')
    return rt('Factura_Egreso.html',ultimo=u[0][2])

@app.route('/Facturacion')
def facturacion():
    cliente=bd.Consultar_datos_especificos(
        ['Nombre','cedula'],
        'usuarios')
    return rt('Facturacion.html',clientes=cliente)

@app.route('/Pago',methods=['POST'])
def abono():
    #variables de informacion
    inf=request.form
    tipo_pago= inf['tipo_pago']
    data_user=inf['data_user']
    fecha=inf['fecha']
    check_placas=[]
    months=[]
    deuda_placa=[]
    solo_placas=[]
    tabla_cobros='cobros_'+str(BW.eb.año)
    #valor=inf['valor']
    
    #recoleccion de datos
    dueño, usercc=cr.dividir_dat(data_user)
    placas = bd.Consultar_datos_especificos(['placa'],
        'vehiculos',where='id_client = '+usercc)
    
    #se recorre el arreglo con las placas para verificar la respuesta
    for u in placas:

        #al ocurrir un error en la consulta de la placa
        #omite y no hace nada,          reecordar 'BaseException' es indispensable
        try:
            check_placas.append(request.form[u[0]])
            #se optienen los meses en deuda de cada placa
            deuda_placa.append(request.form[f'informacion_{u[0]}'])
    
        except BaseException as e:
            #print(e)
            None
        solo_placas.append(u[0])
        
    

    #el tipo de pago define la accion y logica  
    # 
    # al saldar se toma como ingreso el total de la deuda y quedaria con deuda cero 
    rm.definir_pago(tipo_pago,deuda_placa,usercc,BW.valor_mes,
                    solo_placas,check_placas,tabla_cobros,fecha,inf)
    return redirect('/Admin_Fac')
    


@app.route('/Consulta_placa',methods=['POST'])
def cion():
    print(request.form)
    valor=request.form['value']
    datos=bd.Consultar_datos_especificos(
        ['placa','tipo_vehiculo'],
        'vehiculos',where='id_client = '+valor)
    html=''
    for i in datos:
        placa=i[0]
        html+=f'<label for="check_{placa}"style="padding-right: 20px;">'
        html+=f'<b>{i}</b></label><input style="width: 35px;" type="checkbox"'
        html+=f' name="{placa}" id="check_{placa}" value="{placa}">'
    #html+='</div>'
    return rt('respuesta.html',contenido=html)

@app.route('/Consulta_deuda_placa',methods=['POST'])
def deuda_cion():   
    id_client= request.form['value']
    html=rm.Consultar_deuda_placa(BW.eb.day.year,
                                id_client,BW.valor_mes,
                                BW.eb.dic_meses)
    return rt('respuesta.html',contenido=html)



@app.route('/Admin_Caja')
def caja():

    tota,cont,disp=rm.Admin_Caja()

    return rt('Admin_Caja.html',total=tota,contenido=cont,disponible=disp)

@app.route('/Admin_Fac')
def adminfac():
    

    tota,cont = rm.Admin_Fac()
    
    return rt('Admin_Facturas.html',total=tota,contenido=cont)

@app.route('/Eliminar_factura')
def delete_fac():
    None

@app.route('/INVOICE',methods=['POST'])
def c():
    
    rm.INVOICE(request)
    
    return redirect('Admin_Caja')


@app.route('/Registrar_Egreso',methods=['POST'])
def egreso():
    
    rm.Registrar_Egreso(request)
    
    return redirect('/Admin_Caja')


@app.route('/Productos')
def Productos():

    dat,cli,sin_contenido=rm.Productos()

    return rt('Productos.html', dat_colum=dat, Clientes=cli,contenido=sin_contenido)


@app.route('/Producto_Nuevo', methods=['POST'])
def Produt_new():
   
    rm.Producto_Nuevo(request)
    return redirect("/Productos")
   

@app.route('/Editar_producto/<id>')
def edit_produt(id):
    respuesta = bd.Consultar("productos",id,"Codigo")
    return rt("Editar_Producto.html", dat=respuesta[0])

@app.route('/Modificar_Producto/<id>', methods=['POST'])
def Modificar_produt(id):
    rm.Modificar_Producto(request,id)

    return redirect(url_for("Productos"))
  

@app.route('/Eliminar_producto/<string:id>')
def delete_produt(id):
    print(id)
    bd.Consulta_elimina("productos", id)
    return redirect(url_for("Productos"))

if __name__ == '__main__':
    #BW.Cr.registro_masivo_BD()
    app.run(port = 3000,debug= True)