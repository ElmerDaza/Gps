let nuevo = document.getElementById('btn_nuevo');
let datos = document.getElementById('nuevoU');
let conn = document.getElementById("btn_guardar");
nuevo.addEventListener('click',function(){
    'use strict'
    datos.classList.toggle('aparece');
    conn.classList.toggle('aparece');
    
    
});