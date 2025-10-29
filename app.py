from flask import Flask, request, url_for, redirect, render_template, session, jsonify
from datetime import timedelta
from dotenv import load_dotenv
import os
import logging
import sys
from zoneinfo import ZoneInfo

from models.UserModel import UserModel
from models.TaskModel import TaskModel

load_dotenv(dotenv_path='.env')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configurar logging para que salga a stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
logger.info("Logger inicializado correctamente")


@app.route('/')
def index():
    
    return redirect(url_for('registro'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nombre_completo = request.form.get('nombre') + request.form.get('apellido')
        password = request.form.get('password')
        gmail = request.form.get('gmail')
        
        user = UserModel.registro_user(usuario, nombre_completo, password, gmail)
        
        if user[1]=='ok':
            session['id'] = user[0][0]
            session['usuario'] = user[0][1]
            session['nombre_completo'] = user[0][2]

            return redirect(url_for('home'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        user = UserModel.login_user(usuario, password)

        if user[1]=='ok':
            session['id'] = user[0][0]
            session['usuario'] = user[0][1]
            session['nombre_completo'] = user[0][2]

            return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/home', methods=['GET'])
def home():
    
    if 'usuario' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('registro'))

@app.route('/logout')
def logout():
    session.clear()
    
    nombre = session.get('nombre_completo')
    print(nombre)
    
    return jsonify({'location':'registro'})

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    
    data = request.get_json()
    
    nombre_tarea = data['nombre_tarea']
    fecha = data['fecha_limite']
    hora = data['hora_limite']
    id_usuario = session.get('id')
    
    task = TaskModel.agregar_tarea(nombre_tarea,fecha,hora,id_usuario)
    
    print(task)
    
    return jsonify({'status':'ok'})

@app.route('/tareas_usuario')
def tareas_usuario():
    id_usuario = session.get('id')
    
    tareas = TaskModel.tareas(id_usuario)
    
    tareas_dic = []
    
    for t in tareas:
        tarea={
            'idTarea':t[0],
            'idUsuario': t[1],
            'nombreTarea': t[2],
            'fechaTarea': t[3].strftime('%a, %d %b'),
            'horaTarea': str(t[4]) if isinstance(t[4], timedelta) else t[4],
            'realizada': t[5]
        }
        tareas_dic.append(tarea)
    
    return jsonify(tareas_dic)

@app.route('/eliminar_tarea', methods=['GET', 'POST'])
def eliminar_tarea():
    
    data = request.json
    
    id_tarea = data['id_tarea']
    
    tarea_eliminada = TaskModel.eliminar_tarea(id_tarea)
    
    return jsonify({'status':tarea_eliminada})

@app.route('/completar_tarea', methods=['GET','POST'])
def completar_tarea():
    
    data = request.json
    
    id_tarea = data['id_tarea']
    
    print(id_tarea)
    
    tarea_completada = TaskModel.completar_tarea(id_tarea)
    
    print(tarea_completada)
    
    return jsonify({'status':tarea_completada})

@app.route('/tarea_tiempo_limite')
def tarea_tiempo_limite():
    
    zona = repuesto.args.get('zona','UTC)
    
    try:
    	zona_usuario = ZoneInfo(zona)
    except Exception:
        zona_usuario = ZoneInfo('UTC')
        
    logger.info('%s',zona_usuario)
    
    tarea_tiempo_limite = TaskModel.tarea_tiempo_limite(zona_usuario)
    
    return jsonify({'tareas':tarea_tiempo_limite})

@app.route('/perfil', methods=['GET'])
def perfil():
    idUsuario = session.get('id')
    usuario = session.get('usuario')
    
    return jsonify({'idUsuario':idUsuario,'usuario':usuario})

if __name__ == '__main__':
    app.debug = True
    app.run()
