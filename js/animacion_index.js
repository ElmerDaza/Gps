window.addEventListener('scroll', function(){
    let animacion = document.getElementById('obj_animado');
    let position_objec= animacion.getBoundingClientRect().top;
    console.log(position_objec);
    let tamaño_pantalla = window.innerHeight;

    if(position_objec < tamaño_pantalla-15){
        animacion.style.animation = 'mover 4s ease-out'
    }
})