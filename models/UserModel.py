from conexion import obtener_conexion

class UserModel:
    
    @classmethod
    def registro_user(cls, usuario,nombre_completo, password, gmail):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE usuario=%s OR gmail=%s', (usuario,gmail))
        
        resultados = cursor.fetchall()
        
        if resultados:
            return 'nombre o gmail ya ocupados'
        else:
            cursor.execute('INSERT INTO usuarios(usuario,nombreCompleto, password, gmail) VALUES (%s,%s,%s,%s)', (usuario,nombre_completo, password, gmail))
            
            cursor.execute('SELECT id,usuario,nombreCompleto FROM usuarios WHERE usuario=%s AND password=%s', (usuario,password))
            
            user = cursor.fetchone()
            
            return user,'ok'
        
    
    @classmethod
    def login_user(cls, usuario, password):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute('SELECT id,usuario,nombreCompleto FROM usuarios WHERE usuario=%s AND password=%s', (usuario,password))
        
        user = cursor.fetchone()
        
        return user,'ok'