let btn_menu = document.getElementById('tras');
let nav_lateral = document.getElementById('Nav_Lateral');
let con = document.getElementById("nav_lateral")
btn_menu.addEventListener('click',function(){
    'use strict'
    nav_lateral.classList.toggle('mostrar_menu');
    btn_menu.classList.toggle('mover_boton');
    con.classList.toggle('desaparece');
    
});

