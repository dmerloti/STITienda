from flask import Blueprint, render_template
from database import get_db_connection

servicios_bp = Blueprint('servicios', __name__)