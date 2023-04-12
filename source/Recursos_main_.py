import os
import time
import sourse.ClasePDF as P
import BDsql as bd
import source.ClaseRecursos as cr
import sourse.funciones_externas as fe


def definir_pago(tipo_pago:str,deuda_placa:list,
                usercc,valor_mes:int,solo_placas:list,
                check_placas:list,tabla_cobros:str,fecha,
                inf,):
    #la deuda por placa se suma para dar un total a la factura
    total_deuda=0
    for i in deuda_placa:
        total_deuda+=int(i)

    if tipo_pago=='saldar':

        
        #se consulta la informacion para la factura
        informacion_usuario=bd.Consultar('usuarios',usercc,'cedula')
        informacion_usuario=informacion_usuario[0]
        # se crea la factura con la informacion obtenida
        P.Factura_Venta(informacion_usuario,
                        ['efectivo'],
                        '1148-'+str((total_deuda/valor_mes)),
                        'servicio cobrado a la(s) placas: '+format(solo_placas))
        #se modifican las tablas que contienen la informacion financiera
        try:
            ultimo_caja = bd.Ultimo_Registro('caja','Codigo_Caja')[0]
        except:
            ultimo_caja=[0,0,0]
        todo=[0,'ingresos',int(ultimo_caja[2])+total_deuda,cr.fecha_(),total_deuda]
        bd.Registrar(todo,'caja')
        #continuar por modificar las BD necesarias para el control del dinero
        
        #se registra en la tabla de facturas
        ultimo_caja = bd.Ultimo_Registro('caja','Codigo_Caja')[0]

        bd.Registrar([str(informacion_usuario[0]),str(ultimo_caja[0])],'facturas_ingresos')


        #se obtiene la informacion de la deuda para cada placa
        informacion_placas=[]
        #se recorre el arreglo con las placas que estan selecionadas
        for i in check_placas:
            #agregando informacion
            informacion_placas.append(bd.Consultar(tabla_cobros,i,'placa')[0])
        
        #variable de ayuda
        ayuda_efimera=[]
        # se recorre cada informacion [placa] para suspender su deuda
        for i in informacion_placas:
            #se copia el item i
            ayuda_efimera=[i[0],i[1]]
            #abordamos el rango donde se encuentran los meses en la informacion
            
            for j in range(2,14):
                #al cumplir la condicion se iguala a cero la deuda
                if i[j]!=0 and i[j]!=None and i[j]!='None':
                    ayuda_efimera.append(0)
                elif i[j]==None or i[j]=='None':
                    ayuda_efimera.append(0.0)
                else:
                    ayuda_efimera.append(i[j])
            ayuda_efimera.append(fecha)
            #se modifican los datos en la tabla de cobros
            ayuda_efimera.pop(0)
            bd.Modificar_Usuario(tabla_cobros,i[0],ayuda_efimera,columna='placa')
            
    elif tipo_pago=='abono':
        

        #optenemos el valor pagado
        valor_pago=int(inf['valor_pagado'])

        #confirmamos que este pagando menos que la deuda
        if valor_pago<total_deuda:
            #
            #se consulta la informacion para la factura
            informacion_usuario=bd.Consultar('usuarios',usercc,'cedula')
            informacion_usuario=informacion_usuario[0]
            # se crea la factura con la informacion obtenida
            P.Factura_Venta(informacion_usuario,
                            ['efectivo'],
                            '1148-'+str((valor_pago/valor_mes)),
                            'servicio cobrado a la(s) placas: '+format(solo_placas))
            
            #se modifican las tablas que contienen la informacion financiera
            try:
                ultimo_caja = bd.Ultimo_Registro('caja','Codigo_Caja')[0]
            except:
                ultimo_caja = [0,0,0]
            todo=[0,'ingresos',int(ultimo_caja[2])+total_deuda,cr.fecha_(),valor_pago]
            bd.Registrar(todo,'caja')
            #continuar por modificar las BD necesarias para el control del dinero
            #se registra en la tabla de facturas
            ultimo_caja = bd.Ultimo_Registro('caja','Codigo_Caja')[0]

            bd.Registrar([str(informacion_usuario[0]),str(ultimo_caja[0])],'facturas_ingresos')


            #se obtiene la informacion de la deuda para cada placa
            informacion_placas=[]
            #se recorre el arreglo con las placas que estan selecionadas
            for i in check_placas:
                #agregando informacion
                informacion_placas.append(bd.Consultar(tabla_cobros,i,'placa')[0])
            
            #variable de ayuda
            ayuda_efimera=[]
            ayuda_={}
            valor_monimo=min(deuda_placa)

            if len(valor_monimo)!=0:
                # se recorre cada informacion [placa] para suspender su deuda
                for i in informacion_placas:
                    #se copia el item i
                    ayuda_efimera=[i[0],i[1]]
                    #abordamos el rango donde se encuentran los meses en la informacion
                    
                    for j in range(2,14):
                        #al cumplir la condicion se iguala a cero la deuda
                        if i[j]!=0 and i[j]!=None and i[j]!='None':
                            if int(i[j])<int(valor_pago):
                                ayuda_efimera.append(0)
                                valor_pago=int(valor_pago)-int(i[j])
                            elif int(i[j])==int(valor_pago):
                                ayuda_efimera.append(0)
                                valor_pago=0
                            elif int(i[j])>int(valor_pago):
                                ayuda_efimera.append(int(i[j])-int(valor_pago))
                                valor_pago=0
                        elif i[j]==None or i[j]=='None':
                            ayuda_efimera.append(0.0)
                        else:
                            ayuda_efimera.append(i[j])
                    ayuda_efimera.append(fecha)
                    #se modifican los datos en la tabla de cobros
                    ayuda_efimera.pop(0)
                    ayuda_.update({i[0]:ayuda_efimera})
                for a in ayuda_:
                    bd.Modificar_Usuario(tabla_cobros,a,ayuda_[a],columna='placa')
                
        
    else:
        None


def Consultar_deuda_placa(año_actual,id_client:str,
                            valor_mes:int,dic_meses:dict):
    #se crea el nombre de la tabla y debe contener el año de cobro
    tabla='cobros_'+str(año_actual)
    #se obtiene el nombre del usuario
    nombre=bd.Consultar_datos_especificos(['Nombre'],'usuarios',where="cedula = '"+id_client+"'")
    #se agrega el nombre al html
    html=f'<h4 class="name_cli">{nombre[0]}</h4>'
    resp=[]
    cantidad_deuda=0
    #se almacena las placas que le corresponde a ese usuario
    datos=bd.Consultar_datos_especificos(
        ['placa'],
        'vehiculos',where='id_client = '+id_client)

    #se obtienen los valores de la tabla de cobros
    for dat in datos:
        #manejo de errores sin datos en la consulta
        try:
            resp.append(bd.Consultar(tabla,dat[0],'placa')[0])
        except:
            None
            #html+=
    #se agregan esos valores al html
    for il in resp:
        html+=f'<b style="display: block;margin: 10px 15px;">{il[0]}</b><div id="contenedor_{il[0]}" style="display: flex;flex-wrap: wrap;justify-content: space-between;margin-bottom: 35px;">'
        for o in range(2,14):
            if il[o]!=None and il[o]!=0:
                anchoTotal=150
                alto=25
                pagado=(il[o]*100)/valor_mes
                div_avance=(anchoTotal*pagado)/100
                month=dic_meses[str(o-1)]
                html+='<div>'
                html+=f'<div id="{il[0]}{month}" class="barra" style="display: inline-block;'
                html+=f'margin-right: 10px;border-radius: 3px;width: {anchoTotal}px;height: {alto}px;background: blue;"><b name="valor{month}" id="valor{month}">{il[o]}</b>'
                html+=f'<div class="avance" style="width: {div_avance}px;height: {alto-5}px;margin: 2px 0;background: green;border-radius: 50px;"></div></div>'
                html+=f'<label id="month{il[0]}" for="{il[0]}{month}"'
                html+=f'style="display: inline;position: relative;right: 55px;top: 15px;font-size: 20px;margin: 0;padding: 0;">{month}</label>'
                html+='</div>'
                cantidad_deuda+=int(il[o])
        html+=f'<input type="text" name="informacion_{il[0]}" id="mientras" style="display:none;" value="{cantidad_deuda}">'
        html+='</div>'
        cantidad_deuda=0
    
    return html


def Admin_Caja():
    
    #valores en caja
    Caja = bd.Consulta('caja')
    #variables
    total=[]
    tota=[]
    
    #clientes = bd.Consulta('usuarios')
    cont=False
    
    if(len(Caja)!=0):
        #se rrecorre la cantidad de veces que los registros en caja
        for i in range(0,len(Caja)):
            #se agrega el codigo de caja
            total.append(Caja[i][0])
            #se condiciona que ingresos o egresos no puede estar vacio
            if(len(Caja)!=0):
                #se condiciona a ver si es ingreso o egreso para obtener la fecha
                if(Caja[i][1] == 'ingreso' or Caja[i][1]=='ingresos'):
                    #si es un ingreso se agrega la fecha
                    
                    total.append(Caja[i][3])
                    # obtener el valor
                    total.append(Caja[i][4])

                    #se agrega el nombre de cliente 
                    codigo_cliente=bd.Consultar('facturas_ingresos',Caja[i][0],'Codigo_Caja')

                    
                    n =bd.Consultar('usuarios',codigo_cliente[0][0],'ID_Usuarios')
                    #se verifica que el cliente este activo
                    #de lo contrario se busca en los usuarios eliminados
                    if(len(n)!=0):
                        total.append(n[0][1])
                    else:
                        total.append(bd.Consultar('usuarios_eliminados',codigo_cliente,'ID_Usuarios')[0][1])
            
                    
                else:
                    #se agrega la fecha        
                    total.append(Caja[i][3])
                    #se agrega el valor
                    total.append(Caja[i][4])
                    #se agrega el nombre de usuario
                    total.append('Egreso registrado')

            
            #SE AGREGA EL VALOR TOTAL HASTA ESE MOVIMIENTO
            total.append(Caja[i][2])
            #se agrega el tipo de transaccion
            total.append(Caja[i][1])
            #se agrega a el arreglo de informacion todo el arreglo de una factura
            tota.append(total)
            #se limpia el arreglo utilizado
            total=[]

    else:
        cont=True

    disp=bd.Ultimo_Registro("caja","Codigo_Caja")
    if(len(disp)!=0):
        disp=disp[0][2]
    else:
        disp=00
    
    return tota,cont,disp

def Admin_Fac():

    #valores en caja
    Caja = bd.Consulta('caja')
    #variables
    total=[]
    tota=[]
    
    facturas=bd.Consulta('facturas_ingresos')
    cont=False
    
    if(len(facturas)!=0):

        #se rrecorre la cantidad de veces que los registros en caja
        for i in range(0,len(facturas)):
            #se agrega el codigo de caja
            total.append(facturas[i][1])
            #se condiciona a ver si es ingreso o egreso para obtener la fecha
            if(facturas[i][0] != 'egreso'):
                #si es un ingreso se agrega el valor
                #var=bd.Consultar('ingresos',Caja[i][0],'Codigo_Caja')
                for ij in Caja:
                    if str(ij[0])==str(facturas[i][1]):
                        var=ij[4]
                        fech=ij[3]
                #print('este es var en ingresos: ',var)
                total.append(fech)
                #se agrega el valor
                total.append(var)


                #se agrega el nombre de cliente 
                codigo_cliente=facturas[i][0]

                n =bd.Consultar('usuarios',codigo_cliente,'ID_Usuarios')
                if(len(n)!=0):
                    total.append(n[0][1])
                else:
                    total.append(bd.Consultar('usuarios_eliminados',codigo_cliente,'ID_Usuarios')[0][1])
        
                        
            else:
                #se agrega el valor del egreso
            
                #var=bd.Consultar('egresos',Caja[i][0],'Codigo_Caja')
                for ij in Caja:
                    if str(ij[0])==str(facturas[i][1]):
                        var=ij[4]
                        fech=ij[3]
                #print('este es var en egresos: ',var)
                total.append(fech)
                #se agrega el valor
                total.append(var)
                #se agrega el nombre de usuario
                total.append('Egreso registrado')

        
            #se agrega a el arreglo de informacion todo el arreglo de una factura
            tota.append(total)
            #se limpia el arreglo utilizado
            total=[]

    else:
        cont=True

    return tota,cont

def INVOICE(request):
    #variables
    info_product = []
    valor=0
    todo_ingreso=[]
    todo_caja = ['0']
    precios=[]
    cantidades=[]
    total = 0
    #validacion del metodo post
    if (request.method == 'POST'):
        #recibir datos del formulario
        pago = request.form['pago']
        id = request.form['identificador']
        codigos = request.form['codigos']
        observaciones = request.form['observaciones']
        #se consulta el usuario de la compra
        #usuario = bd.Consultar_Usuario('usuarios',id)[0]
        codigos_clientes = cr.codigo_clientes(id+';')
        #cada cliente se genera una factura con el fin de enviarla
        for m in codigos_clientes:
            #se consulta el ultimo valor registrado en la caja
            ultimo = bd.Ultimo_Registro('caja','Codigo_Caja')
            #se obtiene los codigos en un arreglo
            codig = cr.codigo(codigos+';')
            #se obtiene las cantidades en un arreglo
            cantidades =cr.cantidad(codigos+';')
            
            #llenar los arreglos de las tablas
            i=0
            for e in codig:
                #la tabla solo tiene cuatro columnas
                producto=bd.Consultar('productos',e,'Codigo')[0]
                for s in range(1,len(producto)):
                    #se crea un arreglo con el producto para luego cambiar el valor de cantidad
                    info_product.append(producto[s])
                #en el valor de que representa las cantidades disponibles
                #se hace la resta de la cantidad existente menos la cantidad comprada
                info_product[2] =str(int(producto[3])-int(cantidades[i]))
                #se envia la modificacion del producto y se limpia el arreglo
                bd.Modificar_Usuario('productos',e,info_product)
                info_product=[]
                #se agrega el precio del producto al arreglo
                precios.append(producto[2])
                
                i=i+1
            i=0


            #se condiciona el ultimo registro de la tabla
            if(len(ultimo) == 0):
                #si no tiene registros el total sera la cantidad comprada
                for e in range(0,len(codig)):
                    total = total+(int(precios[e])*int(cantidades[e]))
                #valor de la compra
                valor = total
            else:
                #si tiene registros, el total sera el total del ultimo registro mas el valor de la compra
                for e in range(0,len(codig)):
                    total = total+(int(precios[e])*int(cantidades[e]))
                #valor de la compra
                valor = total
                #valor de la compra mas el ultimo total
                total = total+int(ultimo[0][2])
                #for e in range(0,len(codig)):
                #    total = total+(int(precios[e])*int(cantidades[e]))

            #registro en la caja
            #se agregan datos al arreglo de la tabla caja
            
            todo_caja.append('ingreso')
            todo_caja.append(total)
            todo_caja.append(cr.fecha_())
            todo_caja.append(valor)
            #print(todo_caja)
            bd.Registrar(todo_caja,'caja')

            #se registra el codigo de factura en la tabla 'facturas_ingresos
            ultimo_=bd.Ultimo_Registro('caja','Codigo_Caja')
            print('este es ultimo_: ',ultimo_)
            factura=[m,ultimo_[0][0]]
            print('este es factura: ',factura)
            bd.Registrar(factura,'facturas_ingresos')
            
            #llenado del arreglo para ingresos
            todo_ingreso.append(codigos)
            #suspende la ejecucion por segundos.
            #time.sleep(0.5)
            #obtener el ultimo registro de la caja
            #print(bd.Ultimo_Registro('caja','Codigo_Caja'))
            #res = bd.Ultimo_Registro('caja','Codigo_Caja')
            #condicionar su contenido
            if (len(ultimo_)==0):
                #nunca deveria entrar aqui
                todo_ingreso.append('indefinido')
            else:
                #se agrega el valor del codigo de caja
                todo_ingreso.append(ultimo_[0][0])
            #valor de la compra
            todo_ingreso.append(str(valor))
            todo_ingreso.append(cr.fecha_())
            #hacer el registro en ingresos
            bd.Registrar(todo_ingreso,'ingresos')

            #print(total)
            data=[pago]
            #print(usuario)
            #se crea la factura de esta venta
            usuario = bd.Consultar('usuarios',m,'ID_Usuarios')[0]
            #print(usuario)
            P.Factura_Venta(usuario,data, codigos,observaciones)
            todo_ingreso=[]
            todo_caja=['0']
            precios=[]
            total=0
    
    
def Registrar_Egreso(request):
    
    if request.method == 'POST':
        nombre = request.form['Pagado_a']
        telefono =  request.form['Telefono']
        correo =  request.form['NIT']
        Valor = request.form['Valor']
        direccion  = request.form['Direccion']
        clave=request.form['Consepto']
        fecha = request.form['Fecha']
        Observaciones=request.form['Observaciones']
        ultimo =bd.Ultimo_Registro('caja','Codigo_Caja')
        if(len(ultimo)!=0):
            total = int(ultimo[0][2])-int(Valor)
        else:
            total=int(Valor)
        todo=[0,'egreso',total,cr.fecha_(),Valor]
        bd.Registrar(todo,"caja")
        
        ultimo_registro=bd.Ultimo_Registro('caja','Codigo_Caja')
        if(len(ultimo_registro)!=0):
            bd.Registrar([ultimo_registro[0][1],ultimo_registro[0][0]],'facturas_ingresos')
        bd.Registrar(
            [clave,ultimo_registro[0][0],Valor,fecha],
            'egresos'
        )

        ultimo =bd.Ultimo_Registro('caja','Codigo_Caja')

        P.Comprovante_EgresoCaja(
            nombre,correo,telefono,
            fecha,direccion,Valor,ultimo[0][0],
            clave,Observaciones)


def Productos():
    dat=[]
    name_columnas = bd.Nombre_Columnas("productos")
    cli = bd.Consulta("productos")
    for i in range(len(name_columnas)):
        if i < len(name_columnas):
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return dat,cli,sin_contenido

def Producto_Nuevo(request):
    if request.method == 'POST':
        nombre = request.form['Descripcion']
        #codigo =  request.form['Codigo']
        precio = request.form['Precio']
        cantidad= request.form['Existencia']
        #fecha = R.fecha_hora()
        

        todo = ['0',nombre,precio,cantidad]
        bd.Registrar(todo,'productos')

def Modificar_Producto(request,id):
    if request.method == 'POST':
        nombre = request.form['Descripcion']
        codigo =  request.form['Codigo']
        precio = request.form['Precio']
        cantidad= request.form['Existencia']
        #fecha = R.fecha_hora()

        todo = [nombre, precio,cantidad]
        #en el arreglo que lleva la informacion no incluir el codigo
        bd.Modificar_Usuario("productos",id,todo)

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
    return dat,cli,sin_contenido

def Cliente_Nuevo(request):
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        direccion = request.form['DIRECCION']
        clave=request.form['ID']
        fecha = cr.fecha_()
        

        todo = [0,nombre.strip(),telefono.strip(),correo.strip(),
        Cedula.strip(),direccion.strip(),clave.strip(),fecha]
        bd.Registrar(todo,'usuarios')

def Modificar(request,id):
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        Direccion = request.form['DIRECCION']
        Clave = request.form['ID']
        fecha = request.form['Fecha_Afiliacion']

        todo = [nombre.strip(), 
                telefono.strip(), 
                correo.strip(), 
                Cedula.strip(),
                Direccion.strip(),
                Clave.strip(),
                fecha]
        
        bd.Modificar_Usuario("usuarios",id,todo)

def Vehiculos():
    dat=[]
    usuarios=[]
    name_columnas = bd.Nombre_Columnas("vehiculos")
    cli = bd.Consulta("vehiculos")
    usuarios=bd.Consulta('usuarios')
    for i in range(1,len(name_columnas)+1):
        if i < len(name_columnas):
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i][0]))
    
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return dat, cli, sin_contenido,usuarios

def Vehiculo_Nuevo(request,valor_mes,año_actual):
    if request.method == 'POST':
        usercc= request.form['data_user']
        dueño,usercc=cr.dividir_dat(usercc)
        placa = request.form['Placa']
        gps =  request.form['Modelo_GPS']
        vehiculo = request.form['Descripcion_Vehiculo']
        
        fecha = request.form['Fecha_Instalacion']
        
        tipo = request.form['Tipo_Instalacion']
        peaje=bd.confirmar_existencia('vehiculos','placa',placa.upper())
        if peaje[0][0]==0:
            todo = [0,
                    usercc.strip(),
                    placa.upper().strip(),
                    gps.strip(),
                    vehiculo.strip(),
                    dueño.strip(),
                    'activo',
                    tipo.strip(),
                    fecha]
            #se registra el vehiculo
            bd.Registrar(todo,'vehiculos')
            #se registra en la lista de cobros
            mes=fecha[5:-3]
            
            if mes[0] =='0':
                mes=mes[1:]
            #BW.eb.dic_meses[mes]
            lista_registro=[
                placa.upper().strip(),
                usercc.strip()
            ]
            for i in range(1,13):
                if i==int(mes):
                    lista_registro.append(valor_mes)
                #elif i>int(mes):
                #    lista_registro.append(0)
                else:
                    lista_registro.append(None)
            lista_registro.append(fecha)
            database='cobros_'+str(año_actual)
            if (bd.confirmar_existencia_tabla(database)):
                bd.Registrar(lista_registro,database)
            else:
                bd.TablaNueva(fe.m_.BW.columnas_cobros,database,'vigilantes',tabla_cobro=True)
                bd.Registrar(lista_registro,database)
        else:
            return False,placa
        return True, 'true'
def Editar_Vehiculo(id):
    respuesta = bd.Consultar_Usuario("vehiculos",id)
    clients=bd.Consulta('usuarios')
    for i in clients:
        if i[4]==respuesta[0][1]:
            usercode=[str(i[1]+'*'+i[4]),i[0]]
            break
    return respuesta,clients,usercode
        

def Modificar_Vehiculo(request,id):
    if request.method == 'POST':
        usercc= request.form['data_user']
        dueño,usercc=cr.dividir_dat(usercc)
        placa = request.form['placa']
        gps =  request.form['Modelo_GPS']
        vehiculo = request.form['Descripcion_Vehiculo']
        
        fecha = request.form['Fecha_Instalacion']
        
        tipo = request.form['Tipo_Instalacion']
        estad = request.form.get('estado')
        if estad=='on':
            estado='activo'
        else:
            estado='Suspendido'
        todo = [
            usercc.strip(),
            placa.upper().strip(),
            gps.strip(),
            vehiculo.strip(),
            dueño.strip(),
            estado.strip(),
            tipo.strip(),
            fecha]

        bd.Modificar_Usuario("vehiculos",id,todo)

def Cobranza(request,var):
    retorno = 'cobro_sucesfully.html'
    error='NaN'
    if request.method=='POST':
        tipo = request.form['tipo']
        dia_cobro= request.form['dia_cobranza']
        if tipo=='cobrar_dia_actual':
            if var=='Cobro_wap':
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.cobro_wa()
                    #se termina el proceso de cobro wab
                    time.sleep(5)
                    fe.m_.BW.fun.cerrar_browser()
                else:
                    retorno='cobro_error.html'
            elif var=='Cobro_email':
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.bot_email_send()
                    #BW.bot_wha.start()
                else:
                    retorno='cobro_error.html'
            else:
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.crear_hilo_email()
                    fe.m_.BW.hilo_email.start()
                    fe.m_.BW.cobro_wa()
                    #se termina el proceso de cobro wab
                    time.sleep(5)
                    fe.m_.BW.fun.cerrar_browser()
                else:
                    retorno='cobro_error.html'
        elif tipo=='cobrar_especifico':
            #se cambian los valores necesarios para cobro
            fe.m_.BW.eb.dia=int(dia_cobro)
            fe.m_.BW.eb.dia_str='str'
            if var=='Cobro_wap':
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.cobro_wa()
                    #se termina el proceso de cobro wab
                    time.sleep(5)
                    fe.m_.BW.fun.cerrar_browser()
                else:
                    retorno='cobro_error.html'
            elif var=='Cobro_email':
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.bot_email_send()
                else:
                    retorno='cobro_error.html'
            else:
                terminado, error=fe.m_.BW.proceso_primario()
                if terminado:
                    fe.m_.BW.crear_hilo_email()
                    fe.m_.BW.hilo_email.start()
                    fe.m_.BW.cobro_wa()
                    #se termina el proceso de cobro wab
                    time.sleep(5)
                    fe.m_.BW.fun.cerrar_browser()
                else:
                    retorno='cobro_error.html'
            #se restablesen los valores
            fe.m_.BW.eb.dia=fe.m_.BW.eb.day.day
            fe.m_.BW.eb.dia_str=fe.m_.BW.eb.dt.today().strftime('%A')
        
    if 'cobro_sucesfully.html'==retorno:
        #direccion del archivo
        address=os.getcwd()
        address+='/sourse/texto/ContactosNoCobrados.txt'
        #verifica si existe el documento
        contenido_no_cobro=[]
        if os.path.exists(address):
            #ruta del archivo con los contactos
            
            #se accede al archivo
            archivo = open(address, mode='r', encoding='utf-8')
            for line in archivo.readlines():
                if line !='':
                    contenido_no_cobro.append(line)

        return True,retorno,contenido_no_cobro,error
    else:
        return False, retorno,error

