import os
from sourse import ClaseRecursos as R
#libreria para generar pdf
from fpdf import FPDF
import time ,BDsql as bd
#numeos aleatorios
import random
#fecha
from datetime import datetime as dt


#la fecha debe ser año-mes-dia
def Factura_Pago_Recurrente(usuario,
                            direccion,
                            producto,
                            observaciones,
                            valorMes,
                            fecha, placas:list
                            ):

    #contenido de codigos producto
    
    cantidades=[len(placas)]
    productos=[producto]
    precios=[valorMes]
    cadena=''
    contador=0
    
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = usuario[0]
    cedula = usuario[1]
    telefono=usuario[2]
    #print(usuario[0])
    
    #fpago=datos
    
    total=0
    mes=dt.now()
    mes=mes.month
    NumRecibo = format(random.randrange(10000,19999,3))+'-u'+format(usuario[1])+'-m'+format(mes)#bd.Ultimo_Registro('caja','Codigo_Caja')[0][0]
    

    for e in range(0,len(productos)):
        total = total+(int(precios[e])*int(cantidades[e]))
    total_letra= R.numero_a_letras(total)
    #clase para encabezado
    titulo_header = os.getenv('Nombre_Empresa')
    #datos del encabezado
    meta_dat = os.getenv('encabezado_pagina_pdf_pago_recurrente')
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo_carro_moto.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)

    #agregar texto
    #('with', 'height', 'String')
    
    pdf.cell(w-10, h, 'Señores ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de factura', border=True)
    pdf.cell(w+5, h, 'Fecha de vencimiento',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, format(cedula), border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, format(telefono), border=True)
    pdf.cell(5, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    pdf.cell(w+5,h*2,R.FVencimiento(fecha), border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, format(direccion), border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, 'Riohacha - Colombia',ln=1, border=True)
    pdf.cell(5, h, '')
    pdf.cell(0,h,ln=1)


    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Ítem', border='LT')
    pdf.cell(w+25, h, 'Descripcion', border='T')
    pdf.cell(w+25, h, 'Cantidad', border='T')
    pdf.cell(w+25, h, 'Vr. Unidad',ln=1, border='RT',align='R')


    for i in range(0,len(productos)):
        pdf.set_font(font,'', fz)
        pdf.cell(w, h, str(i+1),border='L')
        pdf.cell(w+25, h, productos[i])
        pdf.cell(w+25, h, format(cantidades[i]))
        pdf.cell(w+25, h, format("{:,}".format(precios[i])),ln=1,border='R',align='R')

    #    pdf.cell(w,h)
    #----------------------
    pdf.cell(((w+25)*3)+w,h*len(productos)+20,ln=1,border='BLR')
    #----------------------

    pdf.cell(135,h,'Total ítems: '+str(len(productos)))
    pdf.cell(w,h,'Total Bruto')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format("{:,}".format(total)), ln=1,align='R')


    pdf.set_font(font,'B', fz)
    pdf.cell(135,h,'Valor en letras:')
    pdf.cell(w,h,'Total a pagar')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format("{:,}".format(total)),ln=1,align='R')

    
    pdf.cell(135,h,total_letra+" pesos.",ln=1)
    pdf.cell(w,h,ln=1)
    

    pdf.set_font(font,'B', fz)
    pdf.cell(140,h,'Condiciones de pago:',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(110,h,'servicio recurrente vence el '+R.FVencimiento(fecha))
    pdf.cell(w,h,'$ '+format("{:,}".format(total)),ln=1)

    pdf.set_font(font,'B', fz+3)
    pdf.cell(0,h,'Observaciones:   ',ln=1)
    #pdf.set_font(font,'', fz)
    pdf.cell(0,h*3,'Facturado a los siguientes disposituvos: ',align='J',ln=1)
    pdf.cell(0,h*3,f'{format(observaciones)} ',align='J',ln=1)
    
    pdf.set_font(font,'', fz)
    pdf.cell(0,h*3,'Medios de pago NEQUI-DAVIPLATA: 3233249021, BANCOLOMBIA: 52620837962 ',align='J',ln=1)
    filename=f'Factura_venta_{NumRecibo}.pdf'
    
    pdf.output('static/pdf/'+filename,'F')
    return filename
    #time.sleep(1)
    #if(enviar_correo):
    #    R.email(usuario[3],filename,usuario[1],contexto='Recurrente')


#factura de venta_____________________
def Factura_Venta(usuario,datos,codigos,observaciones):

    #contenido de codigos producto
    A = codigos+';'
    codigos=R.codigo(A)
    cantidades=R.cantidad(A)
    productos=[]
    precios=[]
    cadena=''
    contador=0
    
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = usuario[1]
    cedula = usuario[4]
    telefono=usuario[2]
    fecha=R.fecha_()
    fpago=datos[0]
    direccion = usuario[5]
    total=0
    try:
        NumRecibo =bd.Ultimo_Registro('caja','Codigo_Caja')[0][0]
    except:
        NumRecibo='100001'
    
    
    

    for e in codigos:
        productos.append(bd.Consultar("productos",e,"Codigo")[0][1])
        precios.append(bd.Consultar("productos",e,"Codigo")[0][2])

    for e in range(0,len(productos)):
        total = float(total)+(float(precios[e])*float(cantidades[e]))
    total_letra= R.numero_a_letras(int(total))
    
    #clase para encabezado
    titulo_header = os.getenv('Nombre_Empresa')
    #datos del encabezado
    meta_dat = os.getenv('encabezado_pagina_pdf_pago_recurrente')
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo_carro_moto.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)

    #agregar texto
    #('with', 'height', 'String')
    
    pdf.cell(w-10, h, 'Señores ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2+25, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(15, h, '')
    pdf.cell(w, h, 'Fecha de factura', border=True,ln=1)
    #pdf.cell(w+5, h, 'Fecha de vencimiento',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+50, h, telefono, border=True)
    pdf.cell(15, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    #pdf.cell(w+5,h*2,'', border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+50, h, 'Riohacha - Colombia',ln=1, border=True)
    pdf.cell(5, h, '')
    pdf.cell(0,h,ln=1)


    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Ítem', border='LT')
    pdf.cell(w+25, h, 'Descripcion', border='T')
    pdf.cell(w+25, h, 'Cantidad', border='T')
    pdf.cell(w+25, h, 'Vr. Unidad',ln=1, border='RT',align='R')


    for i in range(0,len(productos)):
        pdf.set_font(font,'', fz)
        pdf.cell(w, h, str(i+1),border='L')
        pdf.cell(w+25, h, productos[i])
        pdf.cell(w+25, h, cantidades[i])
        pdf.cell(w+25, h, precios[i],ln=1,border='R',align='R')

    #    pdf.cell(w,h)
    #----------------------
    pdf.cell(((w+25)*3)+w,h*len(productos)+20,ln=1,border='BLR')
    #----------------------

    pdf.cell(135,h,'Total ítems: '+str(len(productos)))
    pdf.cell(w,h,'Total Bruto')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total), ln=1,align='R')


    pdf.set_font(font,'B', fz)
    pdf.cell(135,h,'Valor en letras:')
    pdf.cell(w,h,'Total a pagar')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total),ln=1,align='R')

    
    pdf.cell(135,h,total_letra+" pesos.",ln=1)
    pdf.cell(w,h,ln=1)
    

    pdf.set_font(font,'B', fz)
    pdf.cell(140,h,'Condiciones de pago:',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(110,h,'Pago de factura No: '+format(NumRecibo))
    pdf.cell(w,h,'$ '+format(total),ln=1)

    pdf.set_font(font,'B', fz)
    pdf.cell(0,h,'Observaciones:   ',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(0,h*3,observaciones,align='J',ln=1)

    filename=f'__Factura_venta_{NumRecibo}.pdf'

    pdf.output('static/pdf/'+filename,'F')
    #time.sleep(1)
    #R.email(usuario[3],filename,usuario[1])


#Comprovante de egreso________________
def Comprovante_EgresoCaja(
    Nombre,
    NIT,Telefono,
    fech,direct,
    valor,
    Codigo_Caja,
    Consept,
    observaciones):
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = Nombre
    cedula = NIT
    telefono=Telefono
    fecha=fech
    fpago='efectivo'
    direccion=direct
    total=valor
    total_letra=R.numero_a_moneda(int(valor))
    NumRecibo = Codigo_Caja
    consepto=Consept

    #clase para encabezado
    titulo_header = os.getenv('Nombre_Empresa')
    #datos del encabezado
    meta_dat = os.getenv('encabezado_pagina_pdf_pago_recurrente')
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo_carro_moto.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)


    #agregar texto
    #('with', 'height', 'String')
    pdf.cell(w-10, h, 'Pagado a ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de pago', border=True)
    pdf.cell(w+5, h, 'Forma de pago',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, telefono, border=True)
    pdf.cell(5, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    pdf.cell(w+5,h*2,fpago, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, 'Riohacha - Colombia',ln=1, border=True)



    pdf.cell(w,h,'',ln=1)
    pdf.cell(w,h,'El valor de ',border=True)
    pdf.cell(135,h,total_letra,border=True)
    pdf.cell(w,h,format(total),border=True,align='R',ln=1)
    pdf.cell(w,h,ln=1)

    pdf.set_font(font,'B',fz)
    pdf.cell(165,h,'Consepto',border=True,align='C')
    pdf.cell(w,h,'Valor',border=True,ln=1)

    pdf.set_font(font,'',fz)
    pdf.cell(165,h,consepto,border=True)
    pdf.cell(w,h,format(total),ln=1,border=True,align='R')


    pdf.cell(135,h)
    pdf.cell(w,h,'Total COP')
    pdf.cell(w,h,format(total),ln=1,align='R')


    pdf.cell(0,4,ln=1)
    pdf.cell(0,h,'Observaciones:',border='LTR',ln=1)
    pdf.cell(0,h*5,observaciones,border='LBR')
    pdf.cell(w*3.25,h*4,'')
    pdf.cell(w*3.25,h*2,'',ln=1)
    pdf.cell(0,h,ln=1)
    pdf.cell(w*3.25,h,'_________________________', align='C')
    pdf.cell(w*3.25,h,'_________________________',align='C',ln=1)
    pdf.cell(w*3.25,h,'Firma elaborado', align='C')
    pdf.cell(w*3.25,h,'Firma recibido',align='C',ln=1)
    pdf.cell(w,h,'')

    filename=f'__Factura_Egreso_{NumRecibo}.pdf'

    pdf.output('static/pdf/egreso/'+filename,'F')


