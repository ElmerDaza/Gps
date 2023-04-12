#explicacion de este archivo:  https://www.youtube.com/watch?v=ZI4XjwbpEwU
#DOCUMENTACION pydryve2: https://docs.iterative.ai/PyDrive2/quickstart/#creating-and-updating-files
#como crear cuenta valida: https://support.google.com/googleapi/answer/6158849/?hl=en&authuser=1
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import os
from sourse import funciones as fun
from source import encryp as en
#________________________________________________
from apiclient import errors
from googleapiclient.http import MediaFileUpload
import httplib2
from googleapiclient.discovery import build

directorio_credenciales = 'credentials_module.json'


#INSTANCIA DE SECION INICIADA
def service():
    #se recupera la llave
    with open('KEYS/'+directorio_credenciales, 'rb') as filekey: 
        key = filekey.read()
    en.decryp(directorio_credenciales,'',key)

    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    #credenciales=login()
    http = httplib2.Http()
    http = gauth.credentials.authorize(http)
    service =build('drive', 'v3', http=http)
    #se encripta el documento de las credenciales
    en.encryp(directorio_credenciales)
    return service
# INICIAR SESION
def login():
    #se recupera la llave
    with open('KEYS/'+os.path.splitext(directorio_credenciales)[0]+'.key', 'rb') as filekey: 
        key = filekey.read()
    en.decryp(directorio_credenciales,'',key)

    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    try:
        if gauth.credentials is None:
            gauth.LocalWebserverAuth(port_numbers=[8092])
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
    except:
        
        direc= os.getcwd()
        direc+="\credentials_module.json"
        sis=os.path.exists('credentials_module.json')
        if sis:
            os.remove(direc)
            print("esta es la exepcion**************************")
            print("esta es**************************"+direc)

        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(directorio_credenciales)
        
        if gauth.credentials is None:
            gauth.LocalWebserverAuth(port_numbers=[8092])
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        

    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    #se encripta el documento de las credenciales
    en.encryp(directorio_credenciales)
    return credenciales

def crear_archivo_texto(nombre_archivo,contenido,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'title': nombre_archivo,\
                                       'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()

#actualizar archivo
def actualizar_archivo(file_name,file_address,id_file, solicitante='exel_bot'):
    '''
    esta funcion actualiza el archivo en drive
        file_name: nombre de archivo
        file_addres: ubicacion del archivo
        id_file: id del archivo en drive
        solicitante: modulo desde donde se ejecuta la actualizacion por defectos en "exel_bot"
    '''
    credencial=login()
    file=credencial.CreateFile({'title':file_name,'id':id_file})
    file.SetContentFile(file_address)
    file.Upload()
    if solicitante=='exel_bot':
        fun.archivo_guardado=True

"""
direccion= os.getcwd()
direccion+="/Archivos/Copia_COBRANZA.xlsx"
nombre='Copia_COBRANZA.xlsx'
actualizar_archivo(nombre,direccion,'1wlW8FcEFXAhcMPp-2LAg8C6Jc5OXwyPp')
"""
# SUBIR UN ARCHIVO A DRIVE
def subir_archivo(ruta_archivo,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    archivo['title'] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

# DESCARGAR UN ARCHIVO DE DRIVE POR ID
def bajar_archivo_por_id(id_drive,ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_drive}) 
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)
    #se encripta el documento
    en.encryp(ruta_descarga + nombre_archivo)
    return nombre_archivo

# BUSCAR ARCHIVOS
def busca(query):
    resultado = []
    credenciales = login()
    # Archivos con el nombre 'mooncode': title = 'mooncode'
    # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
    # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
    # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
    # Archivos en el basurero: trashed=true
    # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        # ID Drive
        print('ID Drive:',f['id'])
        # Link de visualizacion embebido
        print('Link de visualizacion embebido:',f['embedLink'])
        # Link de descarga
        print('Link de descarga:',f['downloadUrl'])
        # Nombre del archivo
        print('Nombre del archivo:',f['title'])
        # Tipo de archivo
        print('Tipo de archivo:',f['mimeType'])
        # Esta en el basurero
        print('Esta en el basurero:',f['labels']['trashed'])
        # Fecha de creacion
        print('Fecha de creacion:',f['createdDate'])
        # Fecha de ultima modificacion
        print('Fecha de ultima modificacion:',f['modifiedDate'])
        # Version
        print('Version:',f['version'])
        # Tamanio
        print('Tamanio:',f['fileSize'])
        resultado.append(f)
    
    return resultado

# DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
def bajar_acrchivo_por_nombre(nombre_archivo,ruta_descarga):
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': "title = '" + nombre_archivo + "'"}).GetList()
    if not lista_archivos:
        print('No se encontro el archivo: ' + nombre_archivo)
    archivo = credenciales.CreateFile({'id': lista_archivos[0]['id']}) 
    archivo.GetContentFile(ruta_descarga + nombre_archivo)
    print(lista_archivos[0]['id'])

# BORRAR/RECUPERAR ARCHIVOS
def borrar_recuperar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    archivo.update()
    # MOVER A BASURERO
    archivo.Trash()
    # SACAR DE BASURERO
    archivo.UnTrash()
    # ELIMINAR PERMANENTEMENTE
    archivo.Delete()

# CREAR CARPETA
def crear_carpeta(nombre_carpeta,id_folder):
    credenciales = login()
    folder = credenciales.CreateFile({'title': nombre_carpeta, 
                               'mimeType': 'application/vnd.google-apps.folder',
                               'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    folder.Upload()

# MOVER ARCHIVO
def mover_archivo(id_archivo,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    propiedades_ocultas = archivo['parents']
    archivo['parents'] = [{'isRoot': False, 
                           'kind': 'drive#parentReference', 
                           'id': id_folder, 
                           'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                           'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
    archivo.Upload(param={'supportsTeamDrives': True})


"""if __name__ == "__main__":

    ruta_archivo = '/home/falv/Escritorio/fondo.jpg'
    id_folder = '0AI_9cD6f9EEZUk9PVA'
    id_drive = '1LVdc-DUwr30kfrA30cVO3K92RVh56pmw'
    ruta_descarga = '/home/falv/Descargas/'
    #crear_archivo_texto('HolaDrive.txt','Hey MoonCoders',id_folder)
    #subir_archivo(ruta_archivo,id_folder)
    #bajar_archivo_por_id(id_drive,ruta_descarga)
    #busca("title = 'mooncode.png'")
    #bajar_acrchivo_por_nombre('Logo_1.png',ruta_descarga)
    #borrar_recuperar('1lHBMFjdyKfAYRa4M57biDZCiDwFhAYTy')
    #crear_carpeta('hola_folder',id_folder)
    mover_archivo('1PmdkaivVUZKkDwFapSWrXNf6n6pO_YK-','1uSMaBaoLOt7F7VJiCZkrO4ckvj6ANecQ')
    """





# ...


def update_file(service, file_id, new_title, new_description, new_mime_type,
                new_filename, new_revision):
  """Update an existing file's metadata and content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to update.
    new_title: New title for the file.
    new_description: New description for the file.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
    new_revision: Whether or not to create a new revision for this file.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()

    # File's new metadata.
    file['title'] = new_title
    file['description'] = new_description
    file['mimeType'] = new_mime_type

    # File's new content.
    media_body = MediaFileUpload(
        new_filename, mimetype=new_mime_type, resumable=True)

    # Send the request to the API.
    updated_file = service.files().update(
        fileId=file_id,
        body=file,
        #newRevision=new_revision,
        media_body=media_body).execute()
    return updated_file
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)
    return None



#service, file_id, new_title, new_description, 
# new_mime_type,
#               new_filename, new_revision):
"""
direccion= os.getcwd()
direccion+="/Archivos/Copia_COBRANZA.xlsx"
a=update_file(service=service(),file_id='',
new_title='titulo nuevo',
new_description='descripcion metadata',
new_mime_type='',new_filename= direccion,new_revision='')
print(a)
"""