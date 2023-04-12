#como buscar con selenium
#https://selenium-python.readthedocs.io/locating-elements.html
from aifc import Error
from sourse import gmail_operation as go, funciones as fun,ClaseRecursos as Cr, drive_operation as do, excel_bot as eb, ClasePDF as pdf
import threading as hilo
import os
import time

#variables
hilo_email=None
FileName=''
ID_FILE= os.getenv('ID_FILE_PRUEBA')
#prueba:# #
Nombre_Archivo='Copia_COBRANZA.xlsx'#'COBRANZA_POR_2021_2022.xlsx'

direccion_empresa=os.getenv('direccion_empresa')
valor_mes=os.getenv('valor_mes')

columnas_cobros = ['placa','id_clientes','enero','febrero','marzo',
                    'abril','mayo','junio','julio','agosto','septiembre',
                    'octubre','noviembre','diciembre','fecha_ultimo_pago']

#_______________________

def cobro_wa():
    #iniciar
    fun.iniciar_browser()
    time.sleep(5)
    #Se ingresa la url del sitio web
    fun.Entrar_Pagina("https://web.whatsapp.com/")
    #descargar archivo de cobranza

    #esperamos que cargue por 5 segundos
    time.sleep(5)
    #esta variable nos dice si hay que esperar
    espera = True
    #whilE para autenticar
    while espera:
        print("ESTOY ESPERANDO")
        #se valida que exista el qr en la pantalla
        espera = fun.valida_qr()
        #se espera 2 segundos
        time.sleep(2)
        #verificar si toca seguir esperando
        if espera == False:
            print("SE AUTENTICO")
            #en caso que no exista el qr se quiebra el lop
            break
    #esperar que cargue
    detente=True
    while detente:
        print("ESTOY ESPERANDO")
        detente = fun.validar_espera()
        time.sleep(2)

    #direccion del archivo
    address=os.getcwd()
    address+='/sourse/texto/ContactosNoCobrados.txt'
    #verifica si existe el documento
    _address=os.path.exists(address)
    if _address:
        os.remove(address)
    #ruta del archivo con los contactos
    ruta='./sourse/texto/contactos_cobro.txt'
    #se accede al archivo
    archivo = open(ruta, mode='r', encoding='utf-8')
    #se examina linea por linea
    #espera de 20 segundos hasta que cargue la pagina
    time.sleep(4)
    
    for contacto in archivo.readlines():
        print('voy a buscar este contacto: '+str(contacto))
        #time.sleep(5)
        #dividir entre deuda, numero y nombre
        numero,nombre,deuda = fun.bisturi(contacto.strip())
        #ingresar a el chat del contacto
        print(nombre)
        try:
            time.sleep(5)
            encontrado=fun.seleccionar_chat(nombre.strip(),numero)
        except Exception as e:
            #bot_whatsapp()
            print("error encontrado de tipo------:",e)
        #solo si es encontrado el contacto se envia mensajes
        if encontrado:
            #espera de 5 second
            time.sleep(1)
            #se envia el mensaje en la siguiente funcion
            #la cual copia el mensaje desde el archivo que se envia
            URL_archivo='./sourse/texto/texto.txt'
            enviado=fun.send_mesage_archivo(URL_archivo,str(contacto.strip()))
            
            if enviado:#si el mensaje fue enviado
                print('informacion enviada')
            else:#en casos que no se envie el mensaje
                if fun.mensajeNoEnviado(contacto):
                    None
                else:
                    contenido=[contacto]
                    fun.crear_archivo_texto(contenido,address)
        else:#en casos que no se envie el mensaje
            if fun.mensajeNoEnviado(contacto):
                None
            else:
                contenido=[contacto]
                fun.crear_archivo_texto(contenido,address)
    
    archivo.close()


#_______________________
def bot_email_send():

    '''
    realiza el envio de emails de cobro a cada usuario 
    tomando la informacion de la base de datos o la workship(hoja de trabajo)
    '''

    global hilo_email
    #"""
    #cobro_wa()
    #"""
    
    #envio de correos
    dic_=eb.dic_DatosArchivoEmail#correo,name,telefono,fecha,[placas]
    #diccionario_placas=eb.dic_vehiculo_cliente
    for k in dic_:
        array_=dic_[k]
        arreglo=[array_[1],k,array_[2]]
        name_file=pdf.Factura_Pago_Recurrente(
            arreglo,direccion_empresa,
            'APP rastreo GPS'
            ,format(array_[4]),
            valor_mes,array_[3],
            array_[4])
        if array_[0]!=None and array_[0]!='None' and array_[0]!='':
            go.enviar_correo_APIgmail_cobro_mensualidad_gps(
                'Facturacion GPS',
                array_[0].strip(),arreglo[0],
                name_file,
                eb.dic_meses[str(eb.mes_actual)])
    
   #Cr.email(array_[0],name_file,array_[1])
        
        

def proceso_primario():
    try:
        direccion= os.getcwd()
        direccion+="/Archivos/"
        #print("------------",direccion)
        eb.file_name=direccion+do.bajar_archivo_por_id(ID_FILE,direccion)
        eb.Nombre_Archivo=Nombre_Archivo
        eb.ID_file=ID_FILE
        #Cr.carga_masivo('usuarios',eb.function_register())
        eb.procesar_datos()
    except Error as e:
        return False, e
    return True, None

def crear_hilo_email():
    global hilo_email
    hilo_email=hilo.Thread(target=bot_email_send)
    #return 
#proceso a ejecutar
#proceso_primario()
#print('terminado')
#fun.terminado()

#hilo1=hilo.Thread(target=cobro_wa)
#iniciar proceso
#hilo1.start()
#bot_wha.start()
#cobro_wa()
#time.sleep(5)

