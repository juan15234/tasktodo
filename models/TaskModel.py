from conexion import obtener_conexion
from datetime import datetime, timedelta, time

class TaskModel:
    
    @classmethod
    def agregar_tarea(cls, nombre_tarea, fechaTarea,horaTarea, id_usuario):
        
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute('''INSERT INTO tareas(idUsuario, nombreTarea, fechaTarea,horaTarea, realizada) VALUES (%s,%s,%s,%s,%s) ''', (id_usuario,nombre_tarea,fechaTarea,horaTarea, 0))
            conexion.commit()
            
            return 'ok'
            
        except Exception as e:
            print(e)
            
            
    @classmethod
    def tareas(cls, id_usuario):
        
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""SELECT * FROM tareas WHERE idUsuario=%s""", (id_usuario))
            
            tareas = cursor.fetchall()
            
            return tareas
            
        except Exception as e:
            print(e)
            
    @classmethod
    def eliminar_tarea(cls, id_tarea):
        
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute('''DELETE FROM tareas WHERE idTarea=%s''', (id_tarea))
            conexion.commit()
            
            return 'ok'
            
        except Exception as e:
            print(e)
            
    @classmethod
    def completar_tarea(cls, id_tarea):
        try:
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute('''UPDATE tareas SET realizada=%s WHERE idTarea=%s''',(1,id_tarea))
            conexion.commit()
            
            return 'ok'
            
        except Exception as e:
            print(e)
            
    @classmethod
    def tarea_tiempo_limite(cls):
        
        hora_actual = datetime.now().time().replace(second=0,microsecond=0)
        fecha_actual = datetime.now().date()
        
        hora_inicio_dia = datetime.now().time().replace(hour=0,minute=0,second=0,microsecond=0)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('''SELECT idTarea, idUsuario, nombreTarea, horaTarea FROM tareas WHERE realizada=%s AND fechaTarea=%s''', (0, fecha_actual))
        
        resultado = cursor.fetchall()
        
        print(hora_actual)
        
        tareas_tiempo_limite = []
        
        for tarea in resultado:
            if isinstance(tarea[3], timedelta):
                total_segundos = int(tarea[3].total_seconds())
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                segundos = total_segundos % 60
                tarea_hora = time(horas, minutos, segundos)
            else:
                tarea_hora = tarea[3]
            print(tarea[0],tarea[1], tarea[2], tarea[3])
            
            if isinstance(tarea_hora, time) and tarea_hora == hora_actual:
                id_tarea_y_usuario = [tarea[0],tarea[1],tarea[2]]
                tareas_tiempo_limite.append(id_tarea_y_usuario)
                
            if isinstance(tarea_hora, time) and tarea_hora == hora_inicio_dia:
                id_tarea_y_usuario = [tarea[0],tarea[1],tarea[2]]
                tareas_tiempo_limite.append(id_tarea_y_usuario)
            
        
        
        print(tareas_tiempo_limite)
        
        return tareas_tiempo_limite