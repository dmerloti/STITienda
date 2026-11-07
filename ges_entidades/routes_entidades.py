from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db_connection
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from ges_seguridad.routes_seguridad import login_required

entidades_bp = Blueprint('entidades', __name__)

#app = Flask(__name__)



# Articulos
@entidades_bp.route('/articulos/articulos')
@login_required
def articulos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select a.id, a.codigo, a.codigoBarras, a.concepto, a.foto, a.precio, a.precioCosto, a.precontado, a.precioVentaMayorista, a.oferta, a.activo, a.existencia, a.puntoReposicion, a.porcentajeGanancia, a.porcentajeGananciaMayorista, a.idrubro, r.concepto as rubro from articulos a left join articulos_rubros r on a.idrubro=r.id  ;")
    articulos=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('articulos/articulos.html',articulos=articulos)

# Create Articulo
@entidades_bp.route('/create_articulo')
def create_articulo():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, concepto FROM articulos_rubros WHERE activo=1")
    rubros = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM proveedores WHERE activo=1")
    proveedores = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM articulos_marcas WHERE activo=1")
    marcas = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM articulos_unidades WHERE activo=1")
    unidades = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM articulos_tipos_iva WHERE activo=1")
    tiposiva = cursor.fetchall()

    return render_template(
        'articulos/create_articulo.html',
        rubros=rubros,
        proveedores=proveedores,
        marcas=marcas,
        unidades=unidades,
        tiposiva=tiposiva
    )
@entidades_bp.route('/guardar_articulo', methods=['POST'])
@login_required
def guardar_articulo():
    _codigo = request.form['txtCodigo']
    _concepto = request.form['txtConcepto']
    _foto = request.files['txtFoto']

    if _codigo == '' or _concepto == '' or _foto.filename == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_articulo'))

    now = datetime.now()
    tiempo = now.strftime("%Y%m%d%H%M%S")

    filename = secure_filename(_foto.filename)
    nuevoNombreFoto = f"{tiempo}_{filename}"

    ruta_foto = os.path.join(app.config['CARPETA'], nuevoNombreFoto)
    _foto.save(ruta_foto)

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos (codigo, concepto, foto)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (_codigo, _concepto, nuevoNombreFoto))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('articulos'))


# Eliminar Articulo
@entidades_bp.route('/destroy_articulo/<id>')
@login_required
def destroy(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# Editar Articulo
@entidades_bp.route('/edit_articulo/<id>')
@login_required
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos WHERE id = %s', (id,))
    articulos=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('articulos/edit_articulo.html', articulos=articulos)

# Actualizar Articulo
@entidades_bp.route('/actualizar_articulo', methods=["POST"])
@login_required
def update():
    id = request.form['txtID']
    _codigo = request.form['txtCodigo']
    _concepto = request.form['txtConcepto']
    _foto = request.files['txtFoto']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Si hay foto nueva
    if _foto and _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save(os.path.join(app.config['CARPETA'], nuevoNombreFoto))

        # Borrar foto anterior
        cursor.execute("SELECT foto FROM articulos WHERE id=%s", (id,))
        fila = cursor.fetchone()
        if fila and fila['foto']:
            ruta_foto = os.path.join(app.config['CARPETA'], fila['foto'])
            if os.path.exists(ruta_foto):
                os.remove(ruta_foto)

        sql = """
            UPDATE articulos
            SET codigo=%s, concepto=%s, foto=%s
            WHERE id=%s
        """
        datos = (_codigo, _concepto, nuevoNombreFoto, id)

    # Si NO se cambia la foto
    else:
        sql = """
            UPDATE articulos
            SET codigo=%s, concepto=%s
            WHERE id=%s
        """
        datos = (_codigo, _concepto, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('articulos'))



# Proveedores
@entidades_bp.route('/proveedores/proveedores')
@login_required
def proveedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.*, l.concepto as localidad, t.concepto as tipo_contribuyente FROM proveedores p LEFT JOIN localidades l ON p.idlocali = l.id LEFT JOIN tipos_contribuyente t ON p.idtipocontribuyente = t.id;")
    proveedores=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('proveedores/proveedores.html',proveedores=proveedores)


# Create Proveedor
@entidades_bp.route('/proveedor_create')
@login_required
def proveedor_create():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, concepto FROM localidades ORDER BY concepto")
    localidades = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM tipos_contribuyente ORDER BY concepto")
    tipos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'proveedores/proveedor_create.html',
        localidades=localidades,
        tipos=tipos
    )

@entidades_bp.route('/proveedor_guardar', methods=['POST'])
@login_required
def proveedor_guardar():

    _cuit = request.form.get('txtCuit')
    _concepto = request.form.get('txtConcepto')
    _celular = request.form.get('txtCelular')
    _mail = request.form.get('txtMail')
    _idlocali = request.form.get('txtLocalidad')
    _idtipo = request.form.get('txtTipoContribuyente')
    _direccion = request.form.get('txtDireccion')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO proveedores
        (cuit, concepto, celular, mail, idlocali, idtipocontribuyente, direccion)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (_cuit,_concepto,_celular,_mail,_idlocali,_idtipo, _direccion))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('entidades.proveedores'))


# Eliminar Proveedor
@entidades_bp.route('/proveedor_destroy/<id>')
@login_required
def proveedor_destroy(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# Editar Proveedor
@entidades_bp.route('/proveedor_edit/<id>')
@login_required
def proveedor_edit(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # proveedor
    cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    proveedor = cursor.fetchone()

    # localidades
    cursor.execute("SELECT id, concepto FROM localidades ORDER BY concepto")
    localidades = cursor.fetchall()

    # tipos contribuyente
    cursor.execute("SELECT id, concepto FROM tipos_contribuyente ORDER BY concepto")
    tipos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'proveedores/proveedor_edit.html',
        proveedor=proveedor,
        localidades=localidades,
        tipos=tipos
    )

# Actualizar Proveedor
@entidades_bp.route('/proveedor_update', methods=["POST"])
@login_required
def proveedor_update():

    id = request.form['txtID']
    _cuit = request.form['txtCuit']
    _concepto = request.form['txtConcepto']
    _celular = request.form['txtCelular']
    _mail = request.form['txtMail']
    _idlocali = request.form['txtLocalidad']
    _idtipo = request.form['txtTipoContribuyente']
    _direccion = request.form['txtDireccion']

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE proveedores
        SET cuit=%s,
            concepto=%s,
            celular=%s,
            mail=%s,
            idlocali=%s,
            idtipocontribuyente=%s,
            direccion=%s
        WHERE id=%s
    """

    datos = (_cuit,_concepto,_celular,_mail,_idlocali,_idtipo, _direccion, id)

    cursor.execute(sql, datos)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('entidades.proveedores'))



#Clientes
@entidades_bp.route('/clientes/clientes')
@login_required
def clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.*, l.concepto as localidad, t.concepto as tipo_contribuyente FROM clientes p LEFT JOIN localidades l ON p.idlocali = l.id LEFT JOIN tipos_contribuyente t ON p.idtipocontribuyente = t.id;")
    clientes=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('clientes/clientes.html',clientes=clientes)


# Create Cliente
@entidades_bp.route('/cliente_create')
@login_required
def cliente_create():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, concepto FROM localidades ORDER BY concepto")
    localidades = cursor.fetchall()

    cursor.execute("SELECT id, concepto FROM tipos_contribuyente ORDER BY concepto")
    tipos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'clientes/cliente_create.html',
        localidades=localidades,
        tipos=tipos
    )

@entidades_bp.route('/cliente_guardar', methods=['POST'])
@login_required
def cliente_guardar():

    _cuit = request.form.get('txtCuit')
    _concepto = request.form.get('txtConcepto')
    _celular = request.form.get('txtCelular')
    _mail = request.form.get('txtMail')
    _idlocali = request.form.get('txtLocalidad')
    _idtipo = request.form.get('txtTipoContribuyente')
    _direccion = request.form.get('txtDireccion')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO clientes
        (cuit, concepto, celular, mail, idlocali, idtipocontribuyente, direccion)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (_cuit,_concepto,_celular,_mail,_idlocali,_idtipo, _direccion))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('entidades.clientes'))


# Eliminar Cliente
@entidades_bp.route('/cliente_destroy/<id>')
@login_required
def cliente_destroy(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('entidades.clientes'))

# Editar Cliente
@entidades_bp.route('/cliente_edit/<id>')
@login_required
def cliente_edit(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # cliente
    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    # localidades
    cursor.execute("SELECT id, concepto FROM localidades ORDER BY concepto")
    localidades = cursor.fetchall()

    # tipos contribuyente
    cursor.execute("SELECT id, concepto FROM tipos_contribuyente ORDER BY concepto")
    tipos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'clientes/cliente_edit.html',
        cliente=cliente,
        localidades=localidades,
        tipos=tipos
    )

# Actualizar Proveedor
@entidades_bp.route('/cliente_update', methods=["POST"])
@login_required
def cliente_update():

    id = request.form['txtID']
    _cuit = request.form['txtCuit']
    _concepto = request.form['txtConcepto']
    _celular = request.form['txtCelular']
    _mail = request.form['txtMail']
    _idlocali = request.form['txtLocalidad']
    _idtipo = request.form['txtTipoContribuyente']
    _direccion = request.form['txtDireccion']

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE clientes
        SET cuit=%s,
            concepto=%s,
            celular=%s,
            mail=%s,
            idlocali=%s,
            idtipocontribuyente=%s,
            direccion=%s
        WHERE id=%s
    """

    datos = (_cuit,_concepto,_celular,_mail,_idlocali,_idtipo, _direccion, id)

    cursor.execute(sql, datos)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('entidades.clientes'))

