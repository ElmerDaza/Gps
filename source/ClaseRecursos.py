# manejo de tiempos
#import time
# importaciones para el email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.base import MIMEBase
from email.encoders import encode_base64
# este modulo permite manejar archuvos
import os,BDsql as bd
#coding: utf-8
# importacion para la fecha
from datetime import datetime
# import para manejo de hilos
import threading
#from xxlimited import Str
# sql
#import BDsql as bd

#cargar informacion masiva ala base de datos
def carga_masivo(tabla:str,contenido:list):
    for i in contenido:
        bd.Registrar(i,tabla)




# ______________________________
#nombre y cedula dividir
def dividir_dat(data:str):
    respuesta=data.split('*')
    return respuesta[0], respuesta[1]


# email
def email(correo_cliente, filename, user_name,asunto = "envio factura de compra", contexto='Recurrente'):
    '''
    Envia correo electronico
        contexto: por defecto es un mensaje recurrente
        correo_cliente: correo de destino
        filename: nombre archivo pdf para adjuntar al correo
        user_name: nombre del destinatario
        asunto: por defecto "envio factura de compra"
    pendiente por colocar la variable "mensaje" que va dentro del html
    '''
    # datos para la cabecera
    remitente = os.getenv('Nombre_Empresa')+'<'+os.getenv('correo_remitente')+'>'
    destino = "Usuario_"+user_name+" <"+correo_cliente+">"
    
    if(contexto == 'Venta'):
        mensajeHTML = "<h1>Hola <b>"+Primera_Palabra(user_name) + \
            "</b></h1>"+\
            "<p style='size: 25px;'>Enviamos la factura de la compra que hiciste el "+format(Dia_Semana())+' '+format(fecha_()) + \
            "</p>"+\
            "<p style='size: 10px;'>este es un mensaje generado <b>automaticamente" +\
            "</b> por favor no responder</p>"
    elif(contexto == 'Recurrente'):
        mensajeHTML="<h1>Hola <b>"+Primera_Palabra(user_name)+"</b></h1>"+\
            "<p style='size: 25px;'>Hoy "+format(Dia_Semana())+' '+format(fecha_())+\
            " te recordamos el pago de la mensualidad para el servicio de monitoreo 24/7.</p>"+\
            "<p style='size: 10px;'>este es un mensaje generado <b>automaticamente" +\
            "</b> por favor no responder</p>"
    ruta_archivo = f'{os.path.abspath(os.getcwd())}\sourse\pdf\ '
    ruta_archivo = ruta_archivo[:-1]+filename
    # print(ruta_archivo)
    # Host y puerto de gmail
    gmail_ = SMTP('smtp.gmail.com', 587)
    # protocolo de cifrado de datos que utiliza gmail
    gmail_.starttls()
    # credenciales de la cuenta
    gmail_.login(os.getenv('correo_remitente'), os.getenv('contraseña_correo_remitente'))
    # depuracion de envio 1=true
    gmail_.set_debuglevel(1)
    # cabecera
    header = MIMEMultipart()
    header['Subject'] = asunto
    header['From'] = remitente
    header['To'] = destino
    mensajeHTML = MIMEText(mensajeHTML, 'html')  # Content-tipe:text/html
    header.attach(mensajeHTML)
    if(os.path.isfile(ruta_archivo)):
        #print('.............existe.............')
        adjunto = MIMEBase('applivcation', 'octer-stream')
        adjunto.set_payload(open(ruta_archivo, 'rb').read())
        encode_base64(adjunto)
        adjunto.add_header(
            'Content-Disposition', 'attachment; filename="%s"' % os.path.basename(ruta_archivo))
        header.attach(adjunto)
    # envia email
    gmail_.sendmail(remitente, destino, header.as_string())
    # cerrar la conexxion
    gmail_.quit()

#________________________________
def FVencimiento(fecha_factura):
    # variables a utilizar
    plazo = 7
    # se divide la fecha en sus valores individuales
    año, mes, dia = Seleccion_año_mes_dia(fecha_factura)
    dat = ''
    # se pasan sus valores a enteros
    mes = int(mes)
    año = int(año)
    # print(mes)
    # se condiciona para saber en que mes se marca
    if(mes == 1):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 2):
        Abisiesto = año % 4
        if(Abisiesto == 0):
            mes = int(mes)
            dia = int(dia)
            dia = dia+plazo
            if(dia > 28):
                dat = f'{año}-{mes+1}-{dia-28}'
            else:
                dat = f'{año}-{mes}-{dia}'
        else:
            mes = int(mes)
            dia = int(dia)
            dia = dia+plazo
            if(dia > 29):
                dat = f'{año}-{mes+1}-{dia-29}'
            else:
                dat = f'{año}-{mes}-{dia}'

    elif(mes == 3):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 4):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 30):
            dat = f'{año}-{mes+1}-{dia-30}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 5):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 6):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 30):
            dat = f'{año}-{mes+1}-{dia-30}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 7):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 8):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 9):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 30):
            dat = f'{año}-{mes+1}-{dia-30}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 10):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{año}-{mes+1}-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 11):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 30):
            dat = f'{año}-{mes+1}-{dia-30}'
        else:
            dat = f'{año}-{mes}-{dia}'

    elif(mes == 12):
        mes = int(mes)
        dia = int(dia)
        dia = dia+plazo
        if(dia > 31):
            dat = f'{int(año)+1}-1-{dia-31}'
        else:
            dat = f'{año}-{mes}-{dia}'
    return dat

#_________________________________
# variable que recibe la fecha en formato año-mes-dia ej: 2019-8-15
def Seleccion_año_mes_dia(fech):
    # variables a utilizar
    añov = ''
    mesv = ''
    diav = ''
    contador = 0
    # se recorre el string
    for i in fech:
        # en caso que no sea un numero se suma 1 al contador
        if(i != '-'):
            # si es un numero se verifica el valor de contador para seleccionar se es año,mes o dia
            if(contador == 0):
                añov += format(i)
            if(contador == 1):
                mesv += format(i)
            if(contador == 2):
                diav += format(i)
        else:
            contador = contador+1
    # se retorna las tres variables con los datos
    return añov, mesv, diav



def fecha_(Hora=False):
    # objeto de fecha
    now = datetime.now()
    # obtener datos individuales
    año = now.year
    mes = now.month
    dia = now.day
    if(Hora == True):
        hora = now.hour
        minuto = now.minute
        segundo = now.second
        # crear un string de la fecha
        dato = "{0}-{1}-{2}-{3}-{4}-{5}".format(año,
                                                mes, dia, 
                                                hora, minuto, 
                                                segundo)
    else:
        # crear un string de la fecha
        dato = "{0}-{1}-{2}".format(año, mes, dia)
    #print(dato)
    return format(dato)


def Dia_Semana(Tipo_Respuesta='vacio'):

    dia = (datetime.today().isoweekday())
    respuesta = ''
    if(dia == 1):
        respuesta = 'lunes'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 2):
        respuesta = 'martes'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 3):
        respuesta = 'miercoles'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 4):
        respuesta = 'jueves'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 5):
        respuesta = 'viernes'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 6):
        respuesta = 'sabado'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    elif(dia == 7):
        respuesta = 'domingo'
        if(Tipo_Respuesta == 'PM'):
            respuesta = respuesta.capitalize()
        elif(Tipo_Respuesta == 'M'):
            respuesta = respuesta.swapcase()
    return respuesta

def Primera_Palabra(cadena:str):
    respuesta = ''
    for i in cadena:
        if(i != ' '):
            respuesta += i
        else:
            break
    return respuesta


def codigo_clientes(codigos_txt):
    cad = ''
    cadena = ''
    codigos = []
    for element in codigos_txt:
        if(element == '0' or element == '1' or element == '2'
                or element == '3' or element == '4' or element == '5'
                or element == '6' or element == '7' or element == '8' or element == '9' or element == '-'):
            cadena += element

        elif(element == ',' or element == ';'):

            codigos.append(cadena)
            cadena = ''
            cad = ''
    return codigos


def codigo(A):
    cad = ''
    cadena = ''
    codigos = []
    for element in A:
        if(element == '0' or element == '1' or element == '2'
                or element == '3' or element == '4' or element == '5'
                or element == '6' or element == '7' or element == '8' or element == '9' or element == '-'):
            cadena += element

        elif(element == ',' or element == ';'):
            for i in range(0, 4):
                cad += cadena[i]
            codigos.append(cad)
            cadena = ''
            cad = ''
    return codigos


def cantidad(A):
    cadena = ''
    cantidades = []
    for element in A:
        if(element == '0' or element == '1' or element == '2'
                or element == '3' or element == '4' or element == '5'
                or element == '6' or element == '7' or element == '8' or element == '9' or element == '-'):
            cadena += element

        elif(element == ',' or element == ';'):

            cantidades.append(cadena[5:])
            cadena = ''

    return cantidades


MONEDA_SINGULAR = 'peso'
MONEDA_PLURAL = 'pesos'

CENTIMOS_SINGULAR = 'centavo'
CENTIMOS_PLURAL = 'centavos'

MAX_NUMERO = 999999999999

UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)

DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

CIENTOS = (
    '_',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)


def numero_a_letras(numero):
    numero_entero = int(numero)
    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        return 'menos %s' % numero_a_letras(abs(numero))
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    if parte_decimal > 9:
        letras_decimal = 'punto %s' % numero_a_letras(parte_decimal)
    elif parte_decimal > 0:
        letras_decimal = 'punto cero %s' % numero_a_letras(parte_decimal)
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    if parte_decimal > 0:
        resultado = '%s %s' % (resultado, letras_decimal)
    return resultado


def numero_a_moneda(numero):
    numero_entero = int(numero)
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    centimos = ''
    if parte_decimal == 1:
        centimos = CENTIMOS_SINGULAR
    else:
        centimos = CENTIMOS_PLURAL
    moneda = ''
    if numero_entero == 1:
        moneda = MONEDA_SINGULAR
    else:
        moneda = MONEDA_PLURAL
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('uno', 'un')
    letras_decimal = 'con %s %s' % (numero_a_letras(
        parte_decimal).replace('uno', 'un'), centimos)
    letras = '%s %s %s' % (letras, moneda, letras_decimal)
    return letras


def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado


def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 0:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado


def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado


def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado


def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))

# print(numero_a_letras(1150000))
