
class Busqueda{
    constructor(selector){
        //variables
        this.selecto=selector;
        this.doc =document;
        //this.parse()
        //this.onInit();
        //this.Buscar()
    }
    
    Buscar(input,selector){
        //agregar evento de tipo cuando suelte la tecla
        this.doc.addEventListener('keyup',(e)=>{
            //console.log(e.target.matches(input));
            //se valida que la informacion venga de input correcto
            if(e.target.matches(input)){
                
                //console.log(e.target.value);
                //se seleccionan y se recorre todos los elementos con la clase de selector
                this.doc.querySelectorAll(selector).forEach((el)=> {
                    //se obtiene el padre del elemnto recorrido
                    let padre = el.parentNode;
                    padre=padre.parentNode;
                    //console.log(padre.parentNode)
                    //se valida el contenido de la cadela en minuscula
                    if(el.textContent.toLowerCase().includes(e.target.value.toLowerCase())){
                        //retirar la clase
                        padre.classList.remove('off')
                
                
                    }else{
                        //agregar la clase
                        padre.classList.add('off');
                    }
                
                });
                
            }
        });
        
    }
    Buscar_producto(input,selector){
        //agregar evento de tipo cuando suelte la tecla
        this.doc.addEventListener('keyup',(e)=>{
            //console.log(e.target.matches(input));
            //se valida que la informacion venga de input correcto
            if(e.target.matches(input)){
                
                //console.log(e.target.value);
                //se seleccionan y se recorre todos los elementos con la clase de selector
                this.doc.querySelectorAll(selector).forEach((el)=> {
                    //se obtiene el padre del elemnto recorrido
                    let padre = el.parentNode;
                    //padre=padre.parentNode;
                    //console.log(padre.parentNode)
                    //se valida el contenido de la cadela en minuscula
                    if(el.textContent.toLowerCase().includes(e.target.value.toLowerCase())){
                        //retirar la clase
                        padre.classList.remove('off')
                
                
                    }else{
                        //agregar la clase
                        padre.classList.add('off');
                    }
                
                });
                
            }
        });
        
    }
      
}
let busqueda = new Busqueda('#datatable');
let busqueda2 = new Busqueda('#selector');
let form = document.getElementById('busquedaForm');
//busqueda.parse();
busqueda.Buscar_producto('.valor','.filtro');
busqueda2.Buscar('.valor2','.filtro2');
//form.addEventListener('submit',()=>{
    
//});