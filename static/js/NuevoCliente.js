let nuevo = document.getElementById('btn_nuevo');
let datos = document.getElementById('nuevoU');
let salir= document.getElementById("salir")
nuevo.addEventListener('click',function(){
    'use strict'
    datos.classList.toggle('aparece');
    
    
});
salir.addEventListener('click',function(){
    datos.classList.toggle('aparece');
})