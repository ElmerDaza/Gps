from ast import Try
from sourse import ClaseRecursos as Cr
import base64
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

# importaciones para el email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.base import MIMEBase
from email.encoders import encode_base64
service=None

CREDENCIALES = 'client_secret.json'
API_NAME='gmail'
API_VERSION='v1'
SCOPES=['https://mail.google.com/']

#___________________________________________
def Create_Service(
    client_secret_file, 
    api_name,
     api_version, *scopes):

    #se recupera la llave
    with open('KEYS/'+os.path.splitext(client_secret_file)[0]+'.key', 'rb') as filekey: 
        key = filekey.read()
    Cr.eb.do.en.decryp(client_secret_file,'',key)
    #print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        try:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
        except:
            try:
                os.remove(pickle_file)
                Create_Service(
                    client_secret_file, 
                    api_name,
                    api_version, scopes[0])
            except:
                None

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        #se encripta el documento de las credenciales
        Cr.eb.do.en.encryp(client_secret_file)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        #se encripta el documento de las credenciales
        Cr.eb.do.en.encryp(client_secret_file)
        return None

def enviar_correo_APIgmail_cobro_mensualidad_gps(
    asunto:str,
    correo_destino:str,
    user_name:str,
    nombre_archivo:str,
    mes:str):
    global service
    if service==None:
        service= Create_Service(CREDENCIALES,API_NAME,API_VERSION,SCOPES)

    MIME_mesage=MIMEMultipart()
    MIME_mesage['subject']=asunto
    MIME_mesage['to']=correo_destino#'notificacionesgeocerca@gmail.com'

    rutaTarjeta='./sourse/texto/mensaje_cobro_email_gps.txt'
    archivo=open(rutaTarjeta, mode='r', encoding='utf-8')
    tarjetaHTML=[]
    menssajeHTML=''
    cont=0
    for lin in archivo.readlines():
        if cont==43:
            tarjetaHTML.append(str(lin)+Cr.Primera_Palabra(user_name))

        elif cont==53:
           tarjetaHTML.append(str(lin)+str(format(Cr.Dia_Semana()))+' <b>'+format(Cr.fecha_())+'</b>')
        elif cont==54:
            tarjetaHTML.append(str(lin)+'<b>'+str(mes)+'</b>')
        else:
            tarjetaHTML.append(str(lin))
        cont=cont+1
    for element in tarjetaHTML:
        menssajeHTML+=str(element)
    archivo.close()
    
    MIME_mesage.attach(MIMEText(menssajeHTML,'html'))

    filename=nombre_archivo


    ruta_archivo = f'{os.path.abspath(os.getcwd())}\static\pdf\ '
    ruta_archivo = ruta_archivo[:-1]+filename


    if(os.path.isfile(ruta_archivo)):
        #print('.............existe.............')
        adjunto = MIMEBase('applivcation', 'octer-stream')
        adjunto.set_payload(open(ruta_archivo, 'rb').read())
        encode_base64(adjunto)
        adjunto.add_header(
            'Content-Disposition', 'attachment; filename="%s"' % os.path.basename(ruta_archivo))
        MIME_mesage.attach(adjunto)
    else:
        print('no existe archivo: ',ruta_archivo)

    try:
        raw_string=base64.urlsafe_b64encode(MIME_mesage.as_bytes()).decode()
        message= service.users().messages().send(userId='me',body={'raw':raw_string}).execute()
        print(message,user_name)
    except:
        print('OCURRIO ERROR AL ENVIAR MENSAJE A: ',user_name)
        service=None
        enviar_correo_APIgmail_cobro_mensualidad_gps(asunto,
                            correo_destino,
                            user_name,nombre_archivo,
                            mes)
    

    
