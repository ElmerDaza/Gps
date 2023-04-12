d= document;
let inp_dia = document.getElementById('inp_');

function dia_unico(){
    
    let w =document.getElementById('cobro_wap')
    let e = document.getElementById('cobro_email')
    
    
    inp_dia.classList.toggle('off')
    inp_dia.classList.toggle('inp_')
    


    
    
}
function cobro_actual(){
    
    let w =document.getElementById('cobro_wap')
    let e = document.getElementById('cobro_email')
    
    
    inp_dia.classList.toggle('off')
    inp_dia.classList.toggle('inp_')
    w.disabled=false
    e.disabled=false
    
    
}
function cobro_action(name_element){
    let form_action = document.getElementById('form_action')
    form_action.action=form_action.action+name_element
    
}