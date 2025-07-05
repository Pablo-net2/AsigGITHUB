from flask import Flask, render_template, jsonify, request, redirect
from ping3 import ping
import time, sqlite3


app = Flask(__name__, static_folder='assets')


    
def trae_nombres(nombrePagina):
    contenido_ip = []
    contenido_nombre = []
    con = sqlite3.connect('setting.db')
    c = con.cursor()
    c.execute(f'Select nombre, ip from pl_connection WHERE pagina = "{nombrePagina}"')
    for i in c:

        
        contenido_nombre.append(i[0])
        contenido_ip.append(i[1])
    con.close()
    return contenido_nombre, contenido_ip
    
def trae_data_locales():
    con = sqlite3.connect('setting.db')
    c = con.cursor()
    c.execute('Select cod, nombre, ip, area, pagina from pl_connection')
    dic = {fila[0]: {'nombre':fila[1], 'ip':fila[2], 'ubicacion':fila[3], 'pagina':fila[4]} for fila in c.fetchall()}
    con.close()
    return dic


@app.route('/')
def servicios():
    segundos = 10
    editar_locales = trae_data_locales()
    contexto = {
        'espacio_tiempo': segundos * 1000,
        'segundo': segundos,
        'editar_locales': editar_locales,
        'pagina': 'Servicios'
    }
    return render_template('servicios.html', **contexto)



def realiza_pings(nombre_dato):
    nombres, ips = trae_nombres(nombre_dato)  # Lista de IPs a hacer ping
    results = {}
    num_pings = 1  # Número de pings a enviar por IP
    delay = 1  # Retraso en segundos entre pings
    nombre_local = ''
    contador = 0
    for ip in ips:
        pings = []

        nombre_local = nombres[contador]
        contador += 1

        for _ in range(num_pings):
            response_time = ping(ip)
            #print(contador, '   --', response_time,'   ', nombre_local, ip)
            if response_time is not None and response_time is not False:
                pings.append(response_time)
            time.sleep(delay)
        
        average_response_time = sum(pings) / len(pings) if pings else None
        estado = 'operativo' if average_response_time != None else 'no-operativo'
        results[ip] = {
            'average_response_time': average_response_time, 
            'estado':estado,
            'local':nombre_local,
            'ping_count': len(pings),
            'espacio_tiempo': 10 * 1000,

        }

    return results


@app.route('/pag_servicios')
def pag_servicios():
    resultado = realiza_pings('Servicios')
    return jsonify(resultado)




@app.route('/edita_local', methods=['POST'])
def edita_local():
    if request.method == 'POST':
        try:
            editar = request.form.get('editId')
            nombre = request.form.get('editName')
            direccion = request.form.get('editDireccion')
            opciones = request.form.get('editOptions')
            paginas = request.form.get('editOptions_paginas')
            conne = sqlite3.connect('setting.db')
            curs = conne.cursor()
            curs.execute(f"UPDATE pl_connection SET nombre='{nombre}', ip='{direccion}', area='{opciones}', pagina='{paginas}' WHERE cod= '{editar}'")

        finally:
            conne.commit()
            conne.close()
            return redirect('/')
        
@app.route('/elimina_local', methods=['GET'])
def elimina_local():
    if request.method == 'GET':
        try:
            eliminar = request.args.get('id')
            conne = sqlite3.connect('setting.db')
            curs = conne.cursor()
            curs.execute(f'DELETE FROM pl_connection WHERE cod= {eliminar}')
            
        except Exception as e:
            print(e)
        finally:
            conne.commit()
            conne.close()
            return redirect('/')
            
@app.route('/nuevo_local',methods=['POST'])
def nuevo_local():
    if request.method == 'POST':
        try:
            nombre = request.form ['name']
            direcc = request.form ['direccion']
            ar = request.form['options']
            pag = request.form['options_paginas']
            msg =  []
            conne = sqlite3.connect('setting.db')
            curs = conne.cursor()
            curs.execute(f"INSERT INTO PL_CONNECTION (nombre, ip, area, pagina) VALUES(?,?,?,?)", (nombre, direcc, ar, pag))
        except Exception as e:
            msg.append(e)

        finally:
            conne.commit()
            conne.close()

            return redirect('/')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)