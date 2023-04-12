import mysql.connector
from mysql.connector import Error
import os
from mysqlx import InterfaceError
from sourse import funciones_externas as fe


HOST=os.getenv('BD_HOST_LOCAL')
USER_NAME=os.getenv('USER_NAME_LOCAL')
PASS=os.getenv('PASS_LOCAL')
BD_NAME=os.getenv('BD_NAME')
#connection 



def Conectar():
    '''
    se conecta a la base de datos 
    y solo se ejecuta si es la primera vez de ejecucion
    o ha ocurrido un error
    '''
    mydb=None
    if mydb==None:
        try:

            mydb = mysql.connector.connect(
                host= (HOST),
                user=(USER_NAME),
                password= (PASS),
                database= (BD_NAME)#,
                #ssl_mode = "VERIFY_IDENTITY",
                #ssl_verify_cert=True,
                #ssl_verify_identity=True
                
                )
                
        except InterfaceError as e:
            mydb=None
            cn = input("escribe 'y' si es afirmativo _")

            if(cn=="y"):
                print(e)
            fe.m_.rt('no_conection_sql.html')


    return mydb

#_______________________________________
def Consulta(tabla):
    try:
        BD = Conectar()
        mycursor = BD.cursor()

        sql = "SELECT * FROM "+tabla 

        mycursor.execute(sql)

        data = mycursor.fetchall()
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE CON UNA BASE DE DATOS__':('")
        print("*************************************")
        print("*******QUIERES VER EL ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")

    
    return data

#________________________________________
def Consulta_elimina(tabla,id):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        Nombre_Column=Nombre_Columnas(tabla)
        cadena = ""
        for i in range(0,len(tabla)):
            cadena+=tabla[i]
        sql="DELETE FROM `{0}` WHERE `{1}` = ('{2}')".format(tabla,Nombre_Column[0][0],id)
        mycursor.execute(sql)
        mycursor.fetchall()
        BD.commit()
        BD.close()
        
        
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE __':('")
        print("*************************************")
        print("*******QUIERES VER EL ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")

#________________________________________
#consultar con la primera columna
def Consultar_Usuario(tabla,id):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        cadena = ""
        for i in range(0,len(tabla)):
            cadena+=tabla[i]
        sql = "SELECT * FROM {0} WHERE ID_{1} = {2}".format(tabla,cadena.capitalize(),id)
        mycursor.execute(sql)

        data = mycursor.fetchall()
        BD.close()
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE CON UNA BASE DE DATOS__':('")
        print("*************************************")
        print("******* ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")
    return data


#________________________________________
def Consultar_datos_especificos(Columnas:list,tabla,where=True):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        colum=''
        for u in Columnas:
            colum+=u+','
        colum=colum[:-1]
        if where==True:
            sql = f"SELECT {colum} FROM {tabla} "
            mycursor.execute(sql)
        else:
            sql = f"SELECT {colum} FROM {tabla} WHERE "+where
            mycursor.execute(sql)
        data = mycursor.fetchall()
        BD.close()
    except:
        print('errrrrrrrrrrrrrrrrrr')
    return data
#________________________________________
#consultar con columna especifica
def Consultar(tabla,id,columna):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        
        sql = "SELECT * FROM {0} WHERE {1} = '{2}'".format(tabla,columna,id)
        mycursor.execute(sql)

        data = mycursor.fetchall()
        BD.close()
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE CON UNA BASE DE DATOS__':('")
        print("*************************************")
        print("******* ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")
    return data



#________________________________________

def Modificar_Usuario(tabla,id, datos,columna=None):#recibe los datos pero sin el numero id
    try:
        #append añade un elemento a la lista
        #datos.append(format(id))
        BD = Conectar()
        mycursor = BD.cursor()
        cadena_tabla = ""
        for i in range(0,len(tabla)):
            cadena_tabla+=tabla[i]

        colum = Nombre_Columnas(tabla)

        if columna==None:


            declaracion = "UPDATE `{0}` SET `{1}`='{2}', ".format(tabla,colum[0][0],id)
            #no enviar el id el la lista de datos
            for i in range(2,len(colum)+1):
                declaracion+= "`{0}`='{1}', ".format(colum[i-1][0],datos[i-2])
            #_______________________
            #borrar el ultimo caracter del string
            declaracion=declaracion[:-1]
            sql=declaracion[:-1]
            sql+=" WHERE {0}='{1}'".format(colum[0][0],id)
            #print(sql)
        else:


            declaracion = "UPDATE `{0}` SET `{1}`='{2}', ".format(tabla,columna,id)
            #no enviar el id el la lista de datos
            for i in range(2,len(colum)+1):
                #if datos[i-2]==None:
                #    declaracion+= "`{0}`=`{1}`, ".format(colum[i-1][0],datos[i-2])
                #else:
                declaracion+= "`{0}`='{1}', ".format(colum[i-1][0],datos[i-2])
            #_______________________
            #borrar el ultimo caracter del string
            declaracion=declaracion[:-1]
            sql=declaracion[:-1]
            sql+=" WHERE {0}='{1}'".format(columna,id)
        
        
        mycursor.execute(sql)
        #print(sql)
        BD.commit()
        BD.close()
        
        
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE CON UNA BASE DE DATOS__':('")
        print("*************************************")
        print("******* ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")
    

#________________________________________
def Nombre_Columnas(tabla):
    data =""
    try:
        
        coneccion = Conectar()
        mycursor = coneccion.cursor()
        mycursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'vigilantes' and TABLE_NAME = '"+tabla+"' order by ORDINAL_POSITION")
        data = mycursor.fetchall()
        
        
    

    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("ERROR EN LOS NOMBRES DE COLUMNA:('")
        print("*************************************")
        print("*******QUIERES VER EL ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")
        

    
    return data

#________________________________________
def Ultimo_Registro(tabla,columna_id):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        sql ='SELECT * FROM {0} ORDER BY {1} DESC LIMIT 1'.format(tabla,columna_id)
        mycursor.execute(sql)

        data = mycursor.fetchall()
        BD.close()
    except Error as e:
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("CONECTATE CON UNA BASE DE DATOS________________________':('")
        print("*************************************")
        print("******* ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")
    return data



#_______________________________________
def Registrar(ArrayValores,tabla):
    try:

        BD = Conectar()
        mycursor = BD.cursor()
        
        colum_name = Nombre_Columnas(tabla)

        vin = "("
        
        for i in range(len(ArrayValores)-1):
            vin += "%s," 

        vin+="%s)"
        col=""
        
        for i in range(len(colum_name)-1):
            col+=format(colum_name[i][0])
            col+=", "

        tam=len(colum_name)-1
        col+=format(colum_name[tam][0])
        
        sql = "INSERT INTO "+tabla+" ("+col+") VALUES "+vin
        

        
        mycursor.execute(sql, ArrayValores)
        BD.commit()
        BD.close()
        
    except Error as e:
        
        print("|")
        print("|")
        print("|")
        print("|")
        print("|")
        print("--------------------------------------------------------")
        print("ERROR AQUI_':('")
        print("*************************************")
        print("*******QUIERES VER EL ERROR**********")
        print("--------------------------------------------------------")
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")

#_________________________________________
def TablaNueva(columnasNAME,tablaNAME,nameBD,tabla_cobro=False):
    dec =""
    sql=''
    BD = Conectar()
    mycursor = BD.cursor()
    le=len(columnasNAME)
    try:
        if tabla_cobro:
            sql='CREATE TABLE `'+nameBD
            +'`.`'+tablaNAME
            +'` (`id_clientes` VARCHAR(50) NOT NULL , `placa` VARCHAR(50) NOT NULL , `enero` BIGINT(50) NULL , `febrero` BIGINT(50) NULL , `marzo` BIGINT(50) NULL , `abril` BIGINT(50) NULL , `mayo` BIGINT(50) NULL , `junio` BIGINT(50) NULL , `julio` BIGINT(50) NULL , `agosto` BIGINT(50) NULL , `septiembre` BIGINT(50) NULL , `octubre` BIGINT(50) NULL , `noviembre` BIGINT(50) NULL , `diciembre` BIGINT(50) NULL , `fecha_ultimo_pago` DATE NULL ) ENGINE = InnoDB;'
        else:
            for i in range (0,le):
                if(columnasNAME[i]!=""):
                    dec +="`"+format(columnasNAME[i])+"` TEXT NOT NULL ,"
            sql=("CREATE TABLE `memori`.`"+tablaNAME+
                "` ( `id` INT(50) NOT NULL AUTO_INCREMENT , "
                +dec+" PRIMARY KEY (`id`)) ENGINE = InnoDB COMMENT = 'un comentario'")
            
        mycursor.execute(sql)
        print("ya cree la tabla _"+tablaNAME+" con las columnas _")
    except Error as e: 
        print("///////////////////////////////////////////////////")
        print("ocurrio un error registrando la tabla")
        print("///////////////////////////////////////////////////")
        print("Quieres ver el error error ")
        
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print("i am sorry! can not understand!   ___"+e)
           
        else:
           print("listo terminé")


def confirmar_existencia_tabla(table_name):
    try:
        bd=Conectar()
        myCursor=bd.cursor()
        sql="SHOW TABLES like '"+table_name+"'"
        myCursor.execute(sql)
        data=myCursor.fetchall()
    except:
        None
    if len(data)==0:
        return False
    else:
        return True

def confirmar_existencia(tabla:str,colum_name:str,id:str):
    try:
        BD = Conectar()
        mycursor = BD.cursor()
        sql=f"SELECT COUNT(*) FROM {tabla} WHERE {colum_name}='{id.format()}'"
        mycursor.execute(sql)
        respuesta=mycursor.fetchall()
        BD.close()
        return respuesta
    except Error as e:
        print('error al consultar el id ',id,'este es el error',e)
