from flask import Blueprint, render_template
from database import get_db_connection

tienda_bp = Blueprint('tienda', __name__)


# INDEX
@tienda_bp.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos where oferta=1 and activo=1 order by concepto;")
    ofertas = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', ofertas=ofertas)


# TIENDA
@tienda_bp.route('/tienda/Tienda')
def tienda():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos where activo=1 or existencia>0 order by concepto;")
    articulos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('tienda.html', articulos=articulos)