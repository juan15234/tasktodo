import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    
    conexion = pymysql.connect(
        user = os.getenv('user_db'),
        host = os.getenv('host'),
        password = os.getenv('password'),
        database = os.getenv('database'),
        port = int(os.getenv('port')),
        autocommit=True
    )

    return conexion