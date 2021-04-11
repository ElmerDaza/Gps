window.addEventListener('scroll', function(){
    let animacion = document.getElementById('obj_animado');
    let position_objec= animacion.getBoundingClientRect().top;
    let animacion_ = document.getElementById('_animado');
    let position_ = animacion_.getBoundingClientRect().top;
    console.log(position_objec);
    let tamaño_pantalla = window.innerHeight;

    if(position_objec < tamaño_pantalla-15 ){
        animacion.style.animation = 'mover 1s ease-out'
    }
    if(position_ < tamaño_pantalla-25){
        animacion_.style.animation = 'mover 1s ease-out'
    }
})