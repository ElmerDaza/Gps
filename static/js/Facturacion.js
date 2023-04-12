let d = document;
arreglo_cod =[];
arreglo_cli=[];
contador =0;
/*selec=d.getElementById('selec');
selec.addEventListener('click',()=>{
    
});*/
d.getElementById('select').addEventListener('change',()=>{
    habilitar_btn();
});
//from = d.getElementById('crearjson');
//from.addEventListener('submit',()=>{
    
    //setTimeout(()=>{
        //from.reset()

    //},10);
//});
function selection_f(id_a){
    identificador=d.getElementById('identificador')
    span_check = d.getElementById('check'+id_a);
    a_select = d.getElementById('select'+id_a)
    identificador.value=''
    if(a_select.ariaSelected=='false'){
        a_select.ariaSelected='true';
        span_check.classList.toggle('selected');
        if (arreglo_cli.length!=0){
            //console.log(arreglo_cli)
            let sn = d.getElementById('check'+arreglo_cli[0])
            let asl=d.getElementById('select'+arreglo_cli[0])
            asl.ariaSelected='false'
            sn.classList.toggle('selected')
            arreglo_cli.shift()
        }
        arreglo_cli.push(id_a);
        //console.log(arreglo_cli)
        
    }else{
        a_select.ariaSelected='false';
        span_check.classList.toggle('selected');
        //identificador.value ='';
        for (let i = 0; i < arreglo_cli.length; i++) {
            const element = arreglo_cli[i];
            if (element === id_a) {
                //si coincide con un valor del array se elimina
                //console.log('---------*');
                cont=arreglo_cli.splice(i,1);
                //console.log(arreglo_cli)
                break;
            }
        }
    }
    arreglo_cli.forEach(e=>{
        identificador.value=identificador.value+e+', ';
    });
    identificador.value=identificador.value.slice(0,-2);
}

function selection(id_a){
    data_user=d.getElementById('data_user')
    span_check = d.getElementById('check'+id_a);
    a_select = d.getElementById('select'+id_a)
    data_user.value=''
    if(a_select.ariaSelected=='false'){
        a_select.ariaSelected='true';
        span_check.classList.toggle('selected');
        if (arreglo_cli.length!=0){
            //console.log(arreglo_cli)
            let sn = d.getElementById('check'+arreglo_cli[0])
            let asl=d.getElementById('select'+arreglo_cli[0])
            asl.ariaSelected='false'
            sn.classList.toggle('selected')
            arreglo_cli.shift()
        }
        name_user=d.getElementById('text'+id_a)
        code_user=d.getElementById('user-code'+id_a)
        data_user.value=name_user.textContent.trim()+'*'+code_user.textContent.trim()
        arreglo_cli.push(id_a);
        //console.log(arreglo_cli)
        
    }else{
        a_select.ariaSelected='false';
        span_check.classList.toggle('selected');
        if(arreglo_cli.length!=0){
            arreglo_cli.shift()
        }
        //identificador.value ='';
        /*for (let i = 0; i < arreglo_cli.length; i++) {
            const element = arreglo_cli[i];
            if (element === id_a) {
                //si coincide con un valor del array se elimina
                //console.log('---------*');
                cont=arreglo_cli.splice(i,1);
                //console.log(arreglo_cli)
                break;
            }
        }*/
    }
    //arreglo_cli.forEach(e=>{
        //identificador.value=identificador.value+e+', ';
    //});
    //identificador.value=identificador.value.slice(0,-2);
}


function selectionALL(){
    selector = d.getElementById('selector').children
    selectALL = d.getElementById('selectALL')
    deselectALL = d.getElementById('deselectALL')
    //textALL = d.getElementById('textALL')
    for (let i = 0; i < selector.length; i++) {
        const e = selector[i];
        if(e.children[0].ariaSelected=="false"){
            id_a=e.className.substr(8);
            selection(id_a)
        }
        
    }
    selectALL.classList.add('off')
    deselectALL.classList.remove('off')
     
    

}
function deselectionALL(){
    selectALL = d.getElementById('selectALL')
    deselectALL = d.getElementById('deselectALL')
    selector = d.getElementById('selector').children
    for (let i = 0; i < selector.length; i++) {
        const e = selector[i].children[0].ariaSelected;
        if(e==="true"){
            //selector[i].children[0].ariaSelected="false"
            id_a=selector[i].className.substr(8);
            selection(id_a)
        }
        
    }
    selectALL.classList.remove('off')
    deselectALL.classList.add('off')
}



function Mostrar(){
    mostrar = d.getElementById('mostrar')
    mostrar.classList.toggle('off')
}

function suprimir(id_a){
    //console.log('---------aquistoy---------')
    //variables
    let eliminar = d.getElementById(id_a+'_');
    let mostrar = d.getElementById(id_a);
    let total = d.getElementById('total');

    let cantProduc = d.getElementById('cant'+id_a.substr(6));
    let precio = d.getElementById('precio'+id_a.substr(6));
    let contenido = '';
    let codigos = d.getElementById('cod');
    let leng = codigos.value.length;
    let cod ='';


    

    // se limpia el campo
    codigos.value='';
    //se recorre el arrego para validar cada elemento
    for (let i = 0; i < arreglo_cod.length; i++) {

        const element = arreglo_cod[i];
        //la variable contiene el valor
        cod=id_a.substr(6)+'-'+cantProduc.innerText
        //console.log(cod)
        //se valida el contenido del elemento
        if (element === cod) {
            //si coincide con un valor del array se elimina
            //console.log('---------')
            
            cont=arreglo_cod.splice(i,1)
            break
        }
    }
    //arreglo_cod = cont;
    arreglo_cod.forEach(element =>{
        codigos.value += element+', '
    });
    codigos.value = codigos.value.slice(0,-2);




    /*
    contenido = codigo(leng,codigos,cod,contenido,id_a,cantProduc);
    console.log(contenido.substr(contenido.length -1));
    if(contenido.substr(contenido.length -1)===' '){
        //console.log('---------ooo------------')
        codigos.value = contenido.slice(0, -2);
    }else{
        codigos.value = contenido;
    }
    */
    'use strict'
    //console.log('---------entre---------');
    //eliminar de la factura
    eliminar.classList.remove('file_fac');
    eliminar.classList.add('off_add')
    //mostrar producto en la lista
    mostrar.classList.remove('off_add');

    //calcular el valor total
    total.innerHTML = parseInt(total.textContent)-(parseInt(cantProduc.textContent)*parseInt(precio.textContent))

    

    habilitar_btn()
    
}


function del_click(id_a){
    //variables y elementos
    agregar = d.getElementById(id_a);
    mostrar = d.getElementById(id_a+'_');
    totalp=d.getElementById('total');
    elnumber = d.getElementById('number'+id_a.substr(6));
    cantProduc = d.getElementById('cant'+id_a.substr(6));
    precio = d.getElementById('precio'+id_a.substr(6));
    hij = [];
    
    codigos = d.getElementById('cod');
  

    //codigos de producto y cantidad----------------------------------------------
    //se limpia el campo
    codigos.value =''
    //se quitan las comas
    //arreglo_cod[arreglo_cod.length]=arreglo_cod[arreglo_cod.length].slice(0,-2)
    //se agrega el contenido sin comas
    arreglo_cod.push(id_a.substr(6)+'-'+elnumber.value);
    //se recorre el arreglo para agregarlo al campo con las comas
    arreglo_cod.forEach(element=>{
        
        codigos.value += element+', ';
    });
    //se eliminan la coma final
    codigos.value=codigos.value.slice(0,-2)
    
    //final de codigos de producto y cantidad------------------------------------





    //se agrega la cantidad a la tabla que se muestra
    cantProduc.innerText = elnumber.value;
    
    //mostrar y ocultar elementos

    'use strict'
    //ocultar producto de la lista
    agregar.classList.add('off_add');
    //mostrar producto en la factura
    mostrar.classList.remove('off_add');
    mostrar.classList.add('file_fac');
    
        
    
    
    tbla= d.getElementById('tb');

    //se obtienen los elementos de la tabla
    for (let i = 0; i < tbla.childElementCount; i++) {
        const element = tbla.children[i];
        hij.push(element);
    }
    //en caso de que el elemento tenga la clase file_fac
    hij.forEach(element => {
       if(element.className==='file_fac'){
           //(element.children[1].innerText = elnumber.value)
       } 
    });
    //calculos para el total
    total= parseInt(totalp.textContent.trim());
    total = total + (parseInt(elnumber.value)*parseInt(precio.textContent.trim()));
    totalp.innerText = total;

    
    habilitar_btn()
}

function registrarEgreso() {
    //alert('epa')
    Pagado_a = document.getElementById('Pagado_a').value;
    Comsepto = document.getElementById('Comsepto').value;
    Fecha = document.getElementById('Fecha').value;
    Valor = document.getElementById('Valor').value;
    total_caja=document.getElementById('t_caja').textContent;
    val=0;
    if(Pagado_a == ''){
        val++;
    }
    if(Comsepto == ''){
        val++;
    }
    if(Fecha == ''){
        val++;
    }
    if(Valor == ''){
        val++;
    }

    if(val == 0){
        console.log(parseInt(Valor,10),parseInt(total_caja,10))
        if (parseInt(Valor,10)>parseInt(total_caja,10)){
            alert('EL VALOR NO PUEDE SER MAYOR A LA CANTIDAD DISPONIBLE.')
            d.getElementById('btn_guardar').disabled=true;

        }else{
            d.getElementById('btn_guardar').disabled=false;
        }
        //console.log('si se puede')
    }else{
        d.getElementById('btn_guardar').disabled=true;
        //console.log('no se puede')
    }
}

function habilitar_btn() {
    codigos=d.getElementById('cod').value;
    identificador=d.getElementById('identificador').value;
    select=d.getElementById('select').value;
    val=0;
    console.log()
    if(codigos == ''){
        val++;
    }
    if(identificador == ''){
        val++;
    }
    if(select == ''){
        val++;
    }
    if(val == 0){
        d.getElementById('btn_guardar').disabled=false;
        //console.log('si se puede')
    }else{
        d.getElementById('btn_guardar').disabled=true;
        //console.log('no se puede')
    }
}

function valor_abono(select){
    var div_valor_abono= document.getElementById('valor_abono')

    if (select.value=='abono'){
        div_valor_abono.innerHTML='<span id="inp_valor_abono" style="display: block;">introdusca el valor del abono</span>'+
        '<input type="number" name="valor_pagado" style="width: 50%;height: 35px;" id="inp_valor_abono" required>'

    }else if(select.value=='saldar'){
        div_valor_abono.innerHTML=''
    }else{
        div_valor_abono.innerHTML='<span id="inp_valor_abono" style="display: block;">introdusca el valor del adelanto</span>'+
        '<input type="number" name="valor_pagado" style="width: 50%;height: 35px;" id="inp_valor_abono" required min="100">'

    }
}

/*function dato_nombre(){
    //console.log('aqui estoy-------')
    let id = d.getElementById('identificador');
    let datos_nombre = d.getElementById('dato_nombre');
    let select_cliente = d.getElementById('uno');
    let hij = select_cliente.selectedOptions;
    let clase_hij = hij[0].className;
    if (clase_hij === 'seleccione'){
        console.log('-------nada de seleccion-----------');
        datos_nombre.innerHTML = 'Datos de factura';
        id.value = '';
    }else{
        id.value = clase_hij.substr(7)
        datos_nombre.innerHTML = 'Factura de compra para '+select_cliente.value;
    }
    
    //let option = d.getElementById(clase_hij);
}*/

    

