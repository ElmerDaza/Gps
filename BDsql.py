import mysql.connector

def Conectar():
    try:

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="memori"
            )
    except Exception as e:
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print("i am sorry! can not understand!   ___"+e)
           
        else:
           print("listo terminé")

    
    return mydb

#_______________________________________
def Consulta(query, tabla):
    try:
        BD = Conectar()
        mycursor = BD.cursor()

        sql = "SELECT * FROM "+tabla+" WHERE palabra ='"+query+"'"

        mycursor.execute(sql)

        data = mycursor.fetchall()
    except Exception as e:
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
            print("i am sorry! can not understand!   ___"+e)
           
        else:
           print("listo terminé")

    
    return data

#_______________________________________
def Registrar(palabra,consepto,tabla):
    try:

        BD = Conectar()
        mycursor = BD.cursor()
        sql = "INSERT INTO "+tabla+" (ID, palabra, concepto) VALUES (%s, %s,%s)"
        val = (0, palabra, consepto)
        mycursor.execute(sql, val)
        BD.commit()
    except Exception as e:
        
        print("|")
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
            print("i am sorry! can not understand!   ___"+e)
           
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
    except Exception as e: 
        print("///////////////////////////////////////////////////")
        print("ocurrio un error registrando la tabla")
        print("///////////////////////////////////////////////////")
        print("Quieres ver el error error ")
        
        cn = input("escribe 'y' si es afirmativo _")

        if(cn=="y"):
            print("i am sorry! can not understand!   ___"+e)
           
        else:
           print("listo terminé")
            
    

