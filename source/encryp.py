import os
import random
from cryptography.fernet import Fernet
import time


def encryp(ruta_file:str,retornar_llave=False):
    '''
    este metodo encripta el archivo 3 veces clmll
    y devuelve la ruta del archivo o la llave
        filename: ruta del archivo a encriptar
        retornar_llave: si es True no crea el archivo y retorna la llave
    '''
    # se genera la llave de encriptacion
    key = Fernet.generate_key()
    ruta, nombre_file=os.path.split(ruta_file)
    nombre_file,extencion_file=os.path.splitext(nombre_file)
    #se guarda la llave en un archivo con el nombre_file.key
    al=f'KEYS/{nombre_file}.key'
    #se verifica que ese archivo no exista
    while(os.path.exists(al)):
        os.remove(al)

    if retornar_llave:
        al= key
    else:
        #guardando la llave en el archivo
        with open(al, 'wb') as filekey: 
            filekey.write(key)
    
    #se inicializa Fernet y se guarda en una variable
    fernet = Fernet(key)
    #print(key)
    for n in range(0,3):
        #se abre el archivo a encriptar
        with open(ruta_file, 'rb') as file: 
            original = file.read() 
        if n==2:
            key=(key[:len(key)-1])
            a=len(key)/2
            b=len(key)
            ke=key[int(a):b]
            key=ke+key[:int(len(key)/2)]+b'='
            #se inicializa Fernet y se guarda en una variable
            #print(key)

            fernet = Fernet(key) 
            #archivo encriptado   
            encrypted = fernet.encrypt(original) 
            #se guarda el archivo encriptado
            with open(ruta_file, 'wb') as encrypted_file: 
                encrypted_file.write(encrypted)
        else:
            #archivo encriptado   
            encrypted = fernet.encrypt(original) 
            #se guarda el archivo encriptado
            with open(ruta_file, 'wb') as encrypted_file: 
                encrypted_file.write(encrypted)
        
        
    #retorna la ruta del archivo o llave
    return al

def decryp(ruta_archivo_encryp:str,ruta_archivo_key,llave=False):
    '''
    desencripta el archivo de la ruta_archivo_encryp 
    utilizando la ruta_archivo_key donde esta la llave 
    o directamente se utiliza la llave
        ruta_archivo_encryp: ruta de archivo encriptado
        ruta_archivo_key: ruta del archivo con la llave
        llave: contiene la llave en caso de no haver archivo
    '''
    if llave==False:
        #se recupera la llave
        with open(ruta_archivo_key, 'rb') as filekey: 
            key = filekey.read()
    else:
        key=llave
    ky=key
    # se inicializa fernet
    key=(key[:len(key)-1])
    a=len(key)/2
    b=len(key)
    ke=key[int(a):b]
    key=ke+key[:int(len(key)/2)]+b'='
    fernet = Fernet(key)
    #print(ke)
    for n in range(0,3):
        #se abre el archivo encriptado
        with open(ruta_archivo_encryp, 'rb') as enc_file: 
            encrypted = enc_file.read() 
        if n==0:
            #se desencripta el archivo
            decrypted = fernet.decrypt(encrypted) 
            #se guarda el archivo desencriptado
            with open(ruta_archivo_encryp, 'wb') as dec_file: 
                dec_file.write((decrypted))
            fernet = Fernet(ky)
        else:
            #se abre el archivo encriptado
            with open(ruta_archivo_encryp, 'rb') as enc_file: 
                encrypted = enc_file.read() 
             #se desencripta el archivo
            decrypted = fernet.decrypt(encrypted) 
            #se guarda el archivo desencriptado
            with open(ruta_archivo_encryp, 'wb') as dec_file: 
                dec_file.write((decrypted))
    if llave is False:
        #se elimina la llave
        os.remove(ruta_archivo_key)
'''ejemplos:
archivo='numeros de cobranza.txt'
ruta_file=encryp(archivo,True)
time.sleep(20)
print('despertando')
decryp(archivo,'',ruta_file)


print('esperando para iniciar el segundo')
#time.sleep(10)
archivo='numeros de cobranza.txt'
ruta_file=encryp(archivo)
time.sleep(20)
print('despertando')
decryp(archivo,ruta_file)'''