from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask import session
from functools import wraps
import mysql.connector
import os
from mysql.connector import Error
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from ges_seguridad.routes_seguridad import seguridad_bp, login_required
from ges_tienda.routes_tienda import tienda_bp
from ges_soporte.routes_soporte import soporte_bp
from ges_entidades.routes_entidades import entidades_bp
from ges_stock.routes_stock import stock_bp
from ges_servicios.routes_servicios import servicios_bp
from ges_ventas.routes_ventas import ventas_bp
from ges_tesoro.routes_tesoro import tesoro_bp
from ges_tablero.routes_tablero import tablero_bp


app = Flask(__name__)
app.secret_key = 'ClaveSecreta'

# Registrar blueprints
app.register_blueprint(seguridad_bp)
app.register_blueprint(tienda_bp)
app.register_blueprint(soporte_bp)
app.register_blueprint(entidades_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(tesoro_bp)
app.register_blueprint(tablero_bp)




# Uploads
CARPETA = os.path.join(os.getcwd(), 'uploads')
app.config['CARPETA'] = CARPETA
os.makedirs(app.config['CARPETA'], exist_ok=True)

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)






# Crear USUARIOS a mano
#@app.route('/crearusuario')
#def crearusuario():

    #conn = get_db_connection()
    #cursor = conn.cursor(dictionary=True)
        
    # Crear usuario DANIEL
    #username = "dmerlo"
    #password = generate_password_hash("s7Inu3V0")
    #rol = "admin"
    #sql = "INSERT INTO usuarios (username, password, rol VALUES (%s, %s, %s)"
    #cursor.execute(sql, (username, password))
    #conn.commit()

    # Crear usuario SILVANA
    #username = "silfa"
    #password = generate_password_hash("silfarrando")
    #sql = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
    #cursor.execute(sql, (username, password))
    #conn.commit()

    #cursor.close()
    #conn.close()








if __name__=='__main__':
    app.run(debug=True)