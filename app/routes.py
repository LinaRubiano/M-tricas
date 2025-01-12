import os
import json
from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

# Ruta del archivo db.json
DB_PATH = 'data/db.json'

# Función para leer los datos desde db.json
def leer_plantas():
    if not os.path.exists(DB_PATH):
        return []  # Si el archivo no existe, devolver una lista vacía
    # Se especifica la codificación 'utf-8' para leer el archivo
    with open(DB_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

# Función para escribir los datos en db.json
def guardar_plantas(plantas):
    # Crear la carpeta 'data' si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Guardar los datos en el archivo db.json
    with open(DB_PATH, 'w') as file:
        json.dump(plantas, file, indent=4)

plants = leer_plantas()

@main.route('/')
def home():
    return render_template('index.html', title='Métricas Verdes')

@main.route('/resumen')
def resumen():
    return render_template('resumen.html', title='Dashboard')

@main.route('/datos-planta')
def datos_planta():
    labels = ['January', 'February', 'March', 'April', 'May', 'June']
    values = [10, 20, 30, 40, 50, 60]

    plantas = leer_plantas()

    return render_template('datos-planta.html', title='Datos Planta', labels=labels, values=values, plantas=plantas)

@main.route('/alertas')
def alertas():
    return render_template('alertas.html', title='alertas')

@main.route('/agregar-planta', methods=['POST'])
def agregar_planta():

    plantas = leer_plantas()

    nueva_planta = {
        'id': len(plantas) + 1,
        'tag': request.form['tag'],
        'species': request.form['species'],
        'germination_date': request.form['germination_date'],
        'initial_conditions': request.form['initial_conditions']
    }
    plantas.append(nueva_planta)

    # Guardar las plantas actualizadas en el archivo
    guardar_plantas(plantas)

    return redirect(url_for('main.datos_planta'))

# @main.route('/handle-planta', methods=['GET'])
# def handle_planta():
#     planta_data = request.args.to_dict()

#     print('Received plant data:', planta_data)

#     return jsonify({'message': 'Plant data received successfully', 'plant': planta_data})

@main.route('/eliminar-planta/<int:id>')
def eliminar_planta(id):

    plantas = leer_plantas()

    # Filtrar la planta a eliminar
    plantas = [planta for planta in plantas if planta['id'] != id]

    # Guardar los cambios en el archivo
    guardar_plantas(plantas)

    return redirect(url_for('main.datos_planta'))
    
def init_app(app):
    app.register_blueprint(main)
