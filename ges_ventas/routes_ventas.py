from flask import Blueprint, render_template
from database import get_db_connection

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/')
def index():
    return render_template('tienda.html')