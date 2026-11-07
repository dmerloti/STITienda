from flask import Blueprint, render_template
from database import get_db_connection

tablero_bp = Blueprint('tablero', __name__)