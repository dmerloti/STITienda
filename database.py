import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'STIStore'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)