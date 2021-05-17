import mysql.connector
from mysql.connector import Error



def Conectar():
    try:

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="vigilantes"
            )
    except Error as e:
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print(e)
           
        else:
           print("listo terminé")

    
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
        cadena = ""
        for i in range(0,len(tabla)):
            cadena+=tabla[i]
        sql="DELETE FROM `{0}` WHERE `ID_{1}` = ('{2}')".format(tabla,cadena.capitalize(),id)
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
def Modificar_Usuario(tabla,id, datos):
    try:
        #append añade un elemento a la lista
        datos.append(format(id))
        BD = Conectar()
        mycursor = BD.cursor()
        cadena = ""
        for i in range(0,len(tabla)):
            cadena+=tabla[i]
        
        sql = "UPDATE `usuarios` SET `Nombre`= '{0}',`Telefono`= '{1}', `Correo`= '{2}', `Cedula`= '{3}',`Clave_Seguridad` = '{4}',`Fecha_afiliacion`='{5}' WHERE ID_{6} = '{7}'".format(
            datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],cadena.capitalize(),datos[6])
        
        mycursor.execute(sql)
        print(sql)
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
        mycursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'vigilantes' and TABLE_NAME = '"+tabla+"'")
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
def TablaNueva(columnasNAME,tablaNAME):
    dec =""
    BD = Conectar()
    mycursor = BD.cursor()
    le=len(columnasNAME)
    try:
        for i in range (0,le):
            if(columnasNAME[i]!=""):
                dec +="`"+format(columnasNAME[i])+"` TEXT NOT NULL ,"

        mycursor.execute(
            "CREATE TABLE `memori`.`"
            +tablaNAME+
            "` ( `id` INT(50) NOT NULL AUTO_INCREMENT , "
            +dec+" PRIMARY KEY (`id`)) ENGINE = InnoDB COMMENT = 'un comentario'"
            )
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
