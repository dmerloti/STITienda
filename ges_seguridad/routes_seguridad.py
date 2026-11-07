from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db_connection

seguridad_bp = Blueprint('seguridad', __name__)

# login
@seguridad_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT u.*, r.concepto AS rol
            FROM usuarios u
            JOIN usuarios_roles r ON u.idrol = r.id
            WHERE u.username = %s
        """
        cursor.execute(sql, (user,))
        user_db = cursor.fetchone()
        conn.close()

        if user_db and check_password_hash(user_db['password'], password):
            session['user'] = user_db['username']
            session['idrol'] = user_db['idrol']
            session['rol'] = user_db['rol']  # admin o vendedor
            return redirect('/')
        else:
            flash("Usuario o contraseña incorrectos - Reintente")
            return redirect('/login')

    return render_template('login.html')

# logout
@seguridad_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tienda.index'))






# proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para ADMIN
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        if session.get('rol') != 'admin':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# Panel de USUARIOS
@seguridad_bp.route('/usuarios')
@admin_required
def usuarios():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT u.id, u.username, r.concepto AS rol
        FROM usuarios u
        JOIN usuarios_roles r ON u.idrol = r.id
    """
    cursor.execute(sql)
    lista = cursor.fetchall()

    conexion.close()

    return render_template('usuarios/usuarios.html', usuarios=lista)


# Crear USUARIOS
@seguridad_bp.route('/usuarios/crear_usuario', methods=['GET', 'POST'])
@admin_required
def crear_usuario():

    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        idrol = request.form['idrol']

        sql = "INSERT INTO usuarios (username, password, idrol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, idrol))
        conexion.commit()

        conexion.close()
        return redirect('/usuarios')

    # Cargar roles para el combo
    cursor.execute("SELECT * FROM usuarios_roles")
    roles = cursor.fetchall()
    conexion.close()

    return render_template('usuarios/crear_usuario.html', roles=roles)


# Editar USUARIO
@seguridad_bp.route('/usuarios/editar_usuario/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_usuario(id):

    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        idrol = request.form['idrol']

        if password:
            password_hash = generate_password_hash(password)
            sql = "UPDATE usuarios SET username=%s, password=%s, idrol=%s WHERE id=%s"
            cursor.execute(sql, (username, password_hash, idrol, id))
        else:
            sql = "UPDATE usuarios SET username=%s, idrol=%s WHERE id=%s"
            cursor.execute(sql, (username, idrol, id))

        conexion.commit()
        conexion.close()

        return redirect('/usuarios')

    # Traer usuario
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    usuario = cursor.fetchone()

    # Traer roles
    cursor.execute("SELECT * FROM usuarios_roles")
    roles = cursor.fetchall()

    conexion.close()

    return render_template('usuarios/editar_usuario.html',
                           usuario=usuario,
                           roles=roles)


# Eliminar USUARIO
@seguridad_bp.route('/usuarios/eliminar/<int:id>')
@admin_required
def eliminar_usuario(id):
    conexion = get_db_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conexion.commit()
    conexion.close()

    return redirect('/usuarios')

# Registro Usuario CLIENTE
@seguridad_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        # Buscar ID del rol cliente
        cursor.execute("SELECT id FROM usuarios_roles WHERE concepto = %s", ('cliente',))
        rol_cliente = cursor.fetchone()

        if not rol_cliente:
            flash("No existe el rol cliente en la base de datos.")
            conexion.close()
            return redirect('/registro')

        idrol = rol_cliente['id']

        # Insertar usuario nuevo
        sql = "INSERT INTO usuarios (username, password, idrol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, idrol))
        conexion.commit()
        conexion.close()

        flash("Usuario creado correctamente.")
        return redirect(url_for('login'))

    return render_template('usuarios/registro.html')

# Roles Usuario
@seguridad_bp.route('/roles')
@login_required
def roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios_roles;")
    roles=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('usuarios/usuarios_roles.html',roles=roles)
