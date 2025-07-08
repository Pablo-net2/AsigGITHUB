function fetchPingResults(fetchUrl, resultContainerId, intervalId) {
    document.getElementById('ejecutando-programa').style.display = 'none';
    mensajeError = `
    <div class="card card-error" >
        <img src="assets/img/nube-triste.jpg" class="card-error-img" alt="img error">

        <div class="card-body">
            <h3 class="card-title">Problemas al realizar ping.</h3>
          <p class="card-text">
            <ul>
                <li>El servidor donde fue levantada la página está sin internet.</li>
                <li>El servidor web está abajo.</li>
            </ul>
          </p>
        </div>
    </div>
    `;
    fetch(fetchUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta de la red');
            }
            return response.json();
        })
        .then(data => {
            //console.log('Datos recibidos:', data); // Depuración
            let resultsHtml = '';
            let segundosEspacio = 0;
            for (const [ip, result] of Object.entries(data)) {
                //console.log('${ result.average_response_time}')
                segundosEspacio = result.espacio_tiempo
                resultsHtml += `
                <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3 col-xxl-3 mb-3">
                    <div class="card ${ 'card-' + result.estado } card-custom">
                        <div class="card-tituloSuperior">
                            ${result.local}
                        </div>
                        <div class="card-body pb-0">
                            <ul type="none">
                                <li class="letraBase">${ip}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                `;
            }
            //<li>ESTADO: ${result.average_response_time !== null && result.average_response_time !== false ? 'Operativo' : 'No operativo'}</li>
            
            document.getElementById(resultContainerId).innerHTML = resultsHtml;
            document.getElementById('ejecutando-programa').style.display = 'block';
            setTimeout(() => fetchPingResults(fetchUrl, resultContainerId, intervalId), segundosEspacio)
            //setTimeout(fetchPingResults, segundosEspacio);
        })
        .catch(error => {
            document.getElementById('ejecutando-programa').innerHTML = mensajeError;
            setTimeout(() => fetchPingResults(fetchUrl, resultContainerId, intervalId), segundosEspacio)
        });
}


document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname;

    // Condicional para determinar cuál página está activa
    if (currentPage === '/') {
        fetchPingResults('/pag_puntoDeVenta', 'ping-results-ventas', 'intervalVentas');
    } else if (currentPage === '/dvr') {
        fetchPingResults('/pag_dvr', 'ping-results-dvr', 'intervalDvr');
    } else if (currentPage === '/servicios') {
        fetchPingResults('/pag_servicios', 'ping-results-servicios', 'intervalServicios');
    }
});


function validaDirr(inputDireccion2) {
    var num_octeto = 1;
    var direccionValidada = false;
    var esPunto = false;
    var charIp = '';
    var cantOcteto = ''
    
    for (let i = 0; i < inputDireccion2.length; i++){
        charIp = inputDireccion2[i];
        
        //Si es str y no un . ERROR 
        if (!isNaN(charIp) != true && charIp != '.') {
            direccionValidada = false;
            break;
        }
        
        if (!isNaN(charIp)){
            esPunto = false;
            cantOcteto = cantOcteto + charIp 
            if (num_octeto === 1){
                if (Number(cantOcteto) >= 223) {
                    direccionValidada = false;
                    break;
                }
            } else if (num_octeto === 2 || num_octeto === 3) {
                if (Number(cantOcteto) >= 255) {
                    direccionValidada = false;
                    break;
                }
            } else if (num_octeto === 4){
                if (Number(cantOcteto) >= 254) {
                    direccionValidada = false;
                    break;
                }
            }
        }else if (charIp == '.'){
            if (esPunto == true){
                direccionValidada = false;  
                break;
            } else {
                num_octeto++
                direccionValidada = true;
                esPunto = true;
                cantOcteto = ''
            }
        }
    }
    return direccionValidada
}

document.getElementById('btnCrear').addEventListener('click', function(event) {
    var form = document.getElementById('nuevoLocal')
    var inputNombre = document.getElementById('name').value;
    var inputDireccion = document.getElementById('direccion').value;
    decide = validaDirr(inputDireccion)
    
    
    if (decide == true){
        if (inputNombre.length != 0){
            alert('Registrado correctamente!!!')
            form.submit();
        }else{
            alert('"Nombre" no valido.')
        }
    } else {
        alert('"Dirección IP" no valida.')
    }
    
})




resultsHtml = `
`


document.getElementById('btnCrearArea').addEventListener('click', function(event) {
    var form = document.getElementById('nuevaArea')
    var inputNombre = document.getElementById('nameArea').value;
    if (inputNombre.length != 0){
        alert('Área registrada correctamente!!!')
        form.submit();
    }else{
        alert('"Nombre" no valido.')
    }   
})

resultsHtml = `
`









const editButtons = document.querySelectorAll('a[id^="btnEditar"]');
editButtons.forEach(link => {
    link.addEventListener('click', function(event) {
        const id = this.getAttribute('data-id');
        const nombre = this.getAttribute('data-nombre');
        const ip = this.getAttribute('data-ip');
        const ubicacion = this.getAttribute('data-ubicacion');
        const pagina = this.getAttribute('data-pagina');

        document.getElementById('editId').value = id;
        document.getElementById('editName').value = nombre;
        document.getElementById('editDireccion').value = ip;
        document.getElementById('editOptions').value = ubicacion;
        document.getElementById('editOptions_paginas').value = pagina;
    });
});








document.getElementById("buscador").addEventListener("input", e => {
    const quitarTildes = (texto) => {
        return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    };

    const textoSinTildes = quitarTildes(e.target.value);

    if (e.target.value === "" && e.inputType === "deleteContentBackward") {
        document.querySelectorAll(".pingsDatos").forEach(anexo => {
            anexo.classList.remove("filtroEditar");
        });
        return;
    }

    document.querySelectorAll(".pingsDatos").forEach(anexo => {
        const textoAnexo = quitarTildes(anexo.textContent.toLowerCase());
        const textoBuscado = textoSinTildes.toLowerCase();

        textoAnexo.includes(textoBuscado)
            ? anexo.classList.remove("filtroEditar")
            : anexo.classList.add("filtroEditar");
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("search");

    form.addEventListener("submit", function(event) {
        // Previene el envío del formulario
        event.preventDefault();
    });
});