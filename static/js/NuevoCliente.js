let nuevo = document.getElementById('btn_nuevo');
let datos = document.getElementById('nuevoU');
let salir= document.getElementById("salir")
let contenido = document.getElementById('content')
nuevo.addEventListener('click',function(){
    'use strict'
    datos.classList.toggle('aparece');
    contenido.classList.toggle('stop')
    
    
});
salir.addEventListener('click',function(){
    datos.classList.toggle('aparece');
})