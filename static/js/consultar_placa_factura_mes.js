
function consulta_ajax(element){
    let valor = element;
    let div_placas = document.getElementById("div_placas");
    $.ajax({
    url:"/Consulta_placa",
    type:"POST",
    data: {"value":valor.slice(6)},
    success: function(response){
        div_placas.innerHTML = response
        div_placas.innerHTML=div_placas.textContent
        //console.log(response)
        //console.log(div_placas)
        
    },
    error: function(error){
        console.log(error);
    }
    
    });
}

function consultar_deuda(idcliente){
    inf_client= document.getElementById('inf_client')
    $.ajax({
        url:"/Consulta_deuda_placa",
        type:"POST",
        data: {"value":idcliente.slice(6)},
        success: function(response){
            inf_client.innerHTML = response
            inf_client.innerHTML=inf_client.textContent
            //console.log(response)
            //console.log(div_placas)
    
        },
        error: function(error){
            console.log(error);
        },
    });
}
function agregar_pago(){
    let placas=[];
    let valor_placas=[];
    let valor_meses=[]
    let tipo_pago=document.getElementById('tipo_pago').value;
    let data_user=document.getElementById('data_user').value;
    let div_placas=document.getElementById('div_placas').getElementsByTagName('INPUT');
    let fecha = document.getElementById('fecha').value
    for (let index = 0; index < div_placas.length; index++) {
        placas.push(div_placas[index].value);
        valor_placas.push(div_placas[index].checked);
        let pago_mes=document.getElementById('contenedor_'+placas[index]);
        let mes=pago_mes.getElementsByTagName('LABEL')[0];
        mes = mes.textContent
        valor =document.getElementById('valor'+mes.textContent)
        valor_meses.push(valor.textContent)

    }
    
}




/*
$(document).ready(function(){
    function consultar_placa(){
        $.ajax({
            url:'/Consulta_placa',
            data:$('form').serialize(),
            type:'POST',
            success: function(response){
                console.log(response)
            },
            error: function(error){
                console.log(error)
            }
        });
    }
    $('#form_datos').submit(function(ev){
        ev.preventDefault();
        consultar_placa()
    });
});*/