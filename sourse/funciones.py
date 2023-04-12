from re import T
import time, os
from sourse import funciones_externas as fun_e
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException as ECIE
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#variables
browser =None
search_result=False
cant_cont_cobrados=0
texto_segunda_linea=''
#esta var se utiliza desde otras clases
archivo_guardado=False


def iniciar_browser():
    global browser
    direccion= os.getcwd()
    servicio = Service(direccion+"\\drivers\\chromedriver.exe")
    occiones= webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=servicio, options=occiones)
    #return browser


#__________________________________
def seleccionar_chat(nombre : str,numero: str):
    contador =0
    #while buscando:
    print("BUSCANDO CHAT")
    
    encontrar = True
    #el bucle continua si contador es menor a 5 y es True
    while encontrar and contador < 5:
        try:
            Span_seleccionado = None
            encontrado = False
            elements=search_elements(numero)
            if elements ==False:
                break
            #se verifica que exista respuesta de la pagina
            while len(elements)==0:
                browser.refresh()
                espera=True
                while espera:
                    print('ESPERANDO QUE CARGUE LA PAGINA')
                    time.sleep(3)
                    espera=validar_espera()
                time.sleep(1)
                elements=search_elements(numero)
            if elements ==False:
                break
            #se fracciona el nombre de contacto condicionando en agun caso que solo tenga un nombre
            dividir=False
            for i in nombre:
                if i == " ":
                    dividir=True
                    break

            if dividir:
                datos = nombre.split(" ")
                
            for element in elements:
                #se convierte a estring el texto del elemento
                Texto_span = str(element.text)
                #se eliminan los posibles espacios al final y al comienzo
                Texto_span = Texto_span.strip()
                #se fracciona el texto por palabras divididas por espacios
                element_palabras = Texto_span.split(" ")
                
                for busqueda in element_palabras:
                    if dividir:
                        if quitar_tildes(busqueda.lower())==quitar_tildes(datos[0].lower()):
                            #print("usuario encontrado")
                            encontrado=True
                            Span_seleccionado=element
                            encontrar = False
                            print("CONTACTO ENCONTRADO.")
                            break
                    else:
                        print('voy a comparar ',busqueda,'y',nombre)
                        if quitar_tildes(busqueda.lower())==quitar_tildes(nombre.lower()):
                            #print("usuario encontrado")
                            encontrado=True
                            Span_seleccionado=element
                            encontrar = False
                            print("CONTACTO ENCONTRADO.")
                            break

                if encontrar!=True:
                    
                    break   
            if encontrar:
                for i in reversed(elements):
                    if str(i.text) != "":
                        encontrado=True

                        Span_seleccionado=i
                        encontrar = False
                        print("SE SELECCIOINO EL PRIMERO...") 
                        break      

        except Exception as e:
            print("NO EXISTE EL NUMERO DE CONTACTO-------------",numero)
            print(e)
            contador = contador+1
            #if contador==5:
            #    del resultado_busqueda
            time.sleep(3)
        
    
    if encontrado:
        global search_result

        while search_result==False:
            time.sleep(3)
            
            search_result=validar_resultado_busqueda()
            if search_result:
                Span_seleccionado.click()
            else:
                seleccionar_chat(nombre,numero)
        search_result=False

        print("encontre_ "+str(contador))
        return encontrado
    else:
        print("CONTACTO NO ENCONTRADO: "+str(nombre))
        print("encontre_ "+str(contador))
        return encontrado

#busqueda de elemenos
def search_elements(numero):
    full_xpat_resultado_busqueda='/html/body/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[1]/div/div'
    full_xpat_resultado_busqueda_='/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div'
    #acceder al elemento de busqueda
    try:
        search = browser.find_element(By.XPATH,'//*[@id="side"]/div[1]/div/label/div/div[2]')
    except:
        try:
            search = browser.find_element(By.XPATH,'//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
        except:
            print('SE DETENDRA EL PROGRAMA DENTRO DE 30s YA QUE NO SE ENCONTRO EL ELEMENTO DE BUSQUEDA:  ')
    #dar clic al elemento
    search.click()
    #agregar el texto a buscar
    search.clear()
    time.sleep(2)
    search.click()
    search.send_keys(numero)
    #esperamos 10 segundos
    time.sleep(10)
    cuadro_busqueda=validar_resultado_busqueda()
    if cuadro_busqueda:
        resultado_busqueda= browser.find_element(By.XPATH, full_xpat_resultado_busqueda)#'//*[@id="pane-side"]/div[1]/div/div/div[2]')
        #elements=resultado_busqueda.find_elements(By.TAG_NAME,'span')
        elements=resultado_busqueda.find_elements(By.CLASS_NAME,'_3q9s6')
        if len(elements)==0:
            resultado_busqueda= browser.find_element(By.XPATH, full_xpat_resultado_busqueda_)#'/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div')
            #elements=resultado_busqueda.find_elements(By.TAG_NAME,'span')
            elements=resultado_busqueda.find_elements(By.CLASS_NAME,'_3vPI2')
    else:
        s_result = sin_resultados()
        if s_result==False:
            search_elements(numero)
        else:
            return False
    return elements


#______________________________________
def send_mesage_archivo(ruta:str,user_txt:str):
    global cant_cont_cobrados
    global texto_segunda_linea

    info_archivo=[]
    dic_vehiculo_cliente=fun_e.variables_exel_bot_cobro_whatsapp()
    #imprimir_diccionario(dic_vehiculo_cliente)
    

    numero,nombre,deuda=bisturi(user_txt.strip())
    placas= dic_vehiculo_cliente[nombre.strip()]
    print(placas)
    nombre_=""
    enviar=False
    for i in nombre:
        if i !=" ":
            nombre_+=i
        else:
            break
    
    archivo = open(ruta, mode='r', encoding='utf-8')
    for linea in archivo.readlines():
        info_archivo.append(linea.strip())


    if cant_cont_cobrados!=0:
        time.sleep(1.3)
        info_archivo[1]=texto_segunda_linea
    else:
        texto_segunda_linea=info_archivo[1]

    
    info_archivo[0]="Buen dia sr@ "+nombre_
    info_archivo[1]+=' para la(s) placa(s): '
    for h in placas:
        if len(placas)!=1:
            info_archivo[1]+='--'+str(h)
        else:
            info_archivo[1]+=str(h)
    #se agrega salto de linea al ultimo elemento
    tamaño=len(info_archivo)
    info_archivo[tamaño-1]+="\n"
    #print(info_archivo)
    archivo.close()
    crear_archivo_texto(info_archivo,ruta)
    
    archivo = open(ruta, mode='r', encoding='utf-8')
    div_user_name= browser.find_element(By.XPATH,'//*[@id="main"]/header/div[2]/div/div')
    span_user_name=div_user_name.find_element(By.TAG_NAME,'span')
    
    user_name=str(span_user_name.text)
    user_name_=user_name.split(' ')
    for b in user_name_:
        if quitar_tildes(b.strip().lower()) == quitar_tildes(nombre_.strip().lower()):
            enviar=True
            print('coinciden los numeros')
            break
    
    #verificar si en vez del nombre esta el numero de contacto
    txt_con_numeros=False
    num=[0,1,2,3,4,5,6,7,8,9]
    numero_contacto=''
    if enviar==False:
        for u in user_name:
            for a in num:
                if u == str(a):
                    numero_contacto+=str(a)
                    txt_con_numeros=True
                    
    if txt_con_numeros:
        
        user_name=get_number(numero_contacto)
        if len(numero_contacto)>9 and len(numero_contacto)<13:
            user_name=user_name[2:]
            if user_name==numero:
                enviar=True       

    #VERIFICAR SI EL NOMBRE NO COINCIDE y tampoco tenga numero
    if enviar ==False:
        try:
            div_user_name.click()
        except ECIE as e:
            print('ha ocurrido un error al dar click en el elemento: ',div_user_name)
            try:
                div_user_name.click()
            except ECIE as e:
                print('error al dar click se reiniciara el metodo: ')
                send_mesage_archivo(ruta,user_txt)
        time.sleep(1.3)
        #en caso de ser empresa
        xpath_empresa='//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[8]/div[3]/div/div/span/span'
        xpath_user='//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/div/span/span'
        xpath_user_='//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/h2/span'
        try:
            contac_num=browser.find_element(By.XPATH,xpath_empresa)
            print('xpath_: ','xpath_empresa')
            numero_contacto= get_number(numero_contacto)
            numero_contacto=numero_contacto[2:]
            if numero_contacto == numero:
                enviar=True
        except:
            try:
                contac_num=browser.find_element(By.XPATH,xpath_user)  
                print('xpath_: ','xpath_user')
            except:
                try:
                    contac_num=browser.find_element(By.XPATH,xpath_user_)
                    print('xpath_: ','xpath_user_')
                except:
                    print('no se logró encontrar el numero para comparar.')
                    return False


            numero_contacto=str(contac_num.text)
            numero_contacto= get_number(numero_contacto)
            numero_contacto=numero_contacto[2:]
            print(numero_contacto)
            #numero_contacto=get_number(str(user_name_[1]+user_name_[2]))

            """x=numero_contacto[len(numero_contacto)-1:]
            numero_contacto,a,d = bisturi(numero_contacto)
            numero_contacto=numero_contacto[2:]
            if len(numero_contacto)== 9:
                numero_contacto+=x"""
            if numero_contacto == numero:
                enviar=True


    if enviar:
        chatbox = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')#'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
        chatbox.click
        try:
            chatbox.send_keys('')
        except:
            try:
                chatbox = browser.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
                chatbox.send_keys('')
            except:
                print('no hay conincidencia en la busqueda del chatbox')
                terminado()
        chatbox.clear()
        contador=1
        for linea in archivo.readlines():
            if linea!="":
                if deuda ==0 and contador < 3:
                    print ("MENSAJE : ", linea)
                    chatbox.send_keys(linea)
                    time.sleep(2)
                    #contador=contador+1
                elif deuda==1 and contador<4:
                    print ("MENSAJE : ", linea)
                    chatbox.send_keys(linea)
                    time.sleep(2)
                    #contador=contador+1

                elif deuda==2 and contador!=3:
                    print ("MENSAJE : ", linea)
                    chatbox.send_keys(linea)
                    time.sleep(2)
            contador=contador+1
        archivo.close()
        #global cant_cont_cobrados
        cant_cont_cobrados=cant_cont_cobrados+1
        return True
    else:
        return False
    

def ventana_nueva(url:str):
    try:
        #nueva ventana
        browser.execute_script("window.open('');")
        #pasar a la nueva ventana
        browser.switch_to.window(browser.window_handles[1])
        #entrar a la url
        browser.get(url)
    except EOFError as e:
        print('error al intentar nueva ventana ',e)
#_________________________________________
def valida_qr():
    try:
        browser.find_element_by_tag_name("canvas")
    except Exception:
        return False
    return True

#________________________________________
#validar espera
def validar_espera():
    try:
        browser.find_element(By.XPATH,'//*[@id="side"]/div[1]/div')
    except:
        return True
    return False

#validar resultado de busqueda
def validar_resultado_busqueda():
    try:
        browser.find_element(By.XPATH,'//*[@id="pane-side"]/div[1]/div/div/div[2]')
    except:
        return False
    return True

#SIN RESULTADOS DE BUSQUEDA
def sin_resultados():
    try:
        s_result = browser.find_element(By.CLASS_NAME,'i0jNr')
        print(s_result.text)
        return True
    except:
        return False

#________________________________________
def cerrar_browser():
    browser.close()
#________________________________________
def Entrar_Pagina(url: str):
    #browser = iniciar_browser()
    browser.get(url)

#________________________________
def tiene_titulo(element):
    elem=str(element.get_attribute("title"))
    if elem!="":
        return True
    else:
        return False
#________________________________
def get_number(txt:str):
    num=[0,1,2,3,4,5,6,7,8,9]
    numero_contacto=''
    
    for u in txt:
        for a in num:
            if u == str(a):
                numero_contacto+=str(a)
                
    return numero_contacto



def bisturi(cadena:str):
    numero,nombre,deuda='','',0
    recolectar_numeros= False
    for i in cadena:
        if (i=='0' or i=='1' or 
            i=='2' or i=='3' or 
            i=='4' or i=='5' or 
            i=='6' or i=='7' or 
            i=='8' or i=='9' and recolectar_numeros):
            numero+=i
        elif (i==":"):
            recolectar_numeros=True
        elif (i=="-"):
            deuda=deuda+1
        else:
            nombre+=i
    return numero,nombre,deuda

def quitar_tildes(cadena:str):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        cadena = cadena.replace(a, b).replace(a.upper(), b.upper())
    return cadena

def terminado():
    try:
        browser.close()
        exit()
    except:
        exit()

#_______________________________
def mensajeNoEnviado(contacto):
    print('no se envio el cobro al usuario -:- ',contacto)
    #direccion del archivo
    address=os.getcwd()
    address+='/sourse/texto/ContactosNoCobrados.txt'
    #verifica si existe el documento
    _address=os.path.exists(address)
    if _address:#si existe se lee y se agrega el usuario nuevo
        file_=open(address,mode='r',encoding='utf-8')
        contenido=[]
        for line in file_.readlines():
            if line!='':
                contenido.append(line)
        contenido.append(contacto)
        crear_archivo_texto(contenido,address)
        file_.close()
    return _address

#___________________________
def crear_archivo_texto(info:list,direccion):
    
    file = open(direccion,"w",encoding="utf8")#w es para escrivir y r es para leer
    for i in range(len(info)):
        if i<len(info)-1:
            file.write(info[i]+"\n")#+format(os.linesep))
        else:
            file.write(info[i])
    file.close()

def imprimir_diccionario(dic_):
    for i in dic_:
        print(i,"-:-", dic_[i])
        print("******************************")
