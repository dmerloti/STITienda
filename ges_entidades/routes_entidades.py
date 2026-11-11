from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db_connection
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from ges_seguridad.routes_seguridad import login_required
from flask import current_app

entidades_bp = Blueprint('entidades', __name__)

#app = Flask(__name__)


# Articulos
@entidades_bp.route('/articulos/articulos')
@login_required
def articulos():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Listado de artículos
    cursor.execute("""
        SELECT
            a.id,
            a.codigo,
            a.codigoBarras,
            a.concepto,
            a.foto,
            a.precio,
            a.precioCosto,
            a.precontado,
            a.precioVentaMayorista,
            a.oferta,
            a.activo,
            a.existencia,
            a.puntoReposicion,
            a.porcentajeGanancia,
            a.porcentajeGananciaMayorista,
            a.idrubro,
            r.concepto AS rubro
        FROM articulos a
        LEFT JOIN articulos_rubros r ON a.idrubro = r.id
        ORDER BY a.concepto
    """)

    articulos = cursor.fetchall()

    # Rubros para el filtro
    cursor.execute("""
        SELECT id, concepto
        FROM articulos_rubros
        WHERE activo = 1
        ORDER BY concepto
    """)

    rubros = cursor.fetchall()
 
    cursor.close()
    conn.close()

    return render_template(
        'articulos/articulos.html',
        articulos=articulos,
        rubros=rubros
    )

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

    # Datos generales
    codigo = request.form.get('txtCodigo')
    codigoBarras = request.form.get('txtCodigoBarras') or None
    concepto = request.form.get('txtConcepto')
    descripcion = request.form.get('txtDescripcion') or None

    # Relaciones
    idrubro = request.form.get('txtRubro') or None
    idproveedor = request.form.get('txtProveedor') or None
    idmarca = request.form.get('txtMarca') or None
    idumedida = request.form.get('txtUnidad') or None
    idtipoiva = request.form.get('txtIVA') or None

    # Cantidades y precios
    puntoReposicion = request.form.get('txtPuntoReposicion') or None
    existencia = request.form.get('txtExistencia') or 0
    dolar = request.form.get('txtDolar') or None
    precio = request.form.get('txtPrecio') or None
    precioCosto = request.form.get('txtPrecioCosto') or None

    # Ganancias y precios de venta
    porcentajeGanancia = request.form.get('txtPorcentajeGanancia') or None
    precontado = request.form.get('txtPrecioMinorista') or None
    porcentajeGananciaMayorista = request.form.get('txtPorcentajeGananciaMayorista') or None
    precioVentaMayorista = request.form.get('txtPrecioMayorista') or None

    # Fechas
    fechaVencimiento = request.form.get('txtFechaVencimiento') or None
    fechaUltimaCarga = request.form.get('txtFechaUltimaCarga') or None

    # Casillas
    activo = 1 if request.form.get('txtActivo') else 0
    oferta = 1 if request.form.get('txtOferta') else 0

    # Validaciones
    if not codigo or not concepto:
        flash('Debe ingresar el código y el concepto del artículo.')
        return redirect(url_for('entidades.create_articulo'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Foto opcional
        foto = request.files.get('txtFoto')
        nuevoNombreFoto = None

        if foto and foto.filename:
            now = datetime.now()
            tiempo = now.strftime("%Y%m%d%H%M%S")
            filename = secure_filename(foto.filename)
            nuevoNombreFoto = f"{tiempo}_{filename}"

            ruta_foto = os.path.join(
                current_app.config['CARPETA'],
                nuevoNombreFoto
            )

            foto.save(ruta_foto)

        sql = """
            INSERT INTO articulos (
                codigo,
                codigoBarras,
                concepto,
                descripcion,
                idrubro,
                idproveedor,
                idmarca,
                puntoReposicion,
                existencia,
                idumedida,
                dolar,
                precio,
                idtipoiva,
                precioCosto,
                porcentajeGanancia,
                precontado,
                porcentajeGananciaMayorista,
                precioVentaMayorista,
                fechaVencimiento,
                fechaUltimaCarga,
                activo,
                oferta,
                foto
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        datos = (
            codigo,
            codigoBarras,
            concepto,
            descripcion,
            idrubro,
            idproveedor,
            idmarca,
            puntoReposicion,
            existencia,
            idumedida,
            dolar,
            precio,
            idtipoiva,
            precioCosto,
            porcentajeGanancia,
            precontado,
            porcentajeGananciaMayorista,
            precioVentaMayorista,
            fechaVencimiento,
            fechaUltimaCarga,
            activo,
            oferta,
            nuevoNombreFoto
        )

        cursor.execute(sql, datos)
        conn.commit()

        flash('Artículo guardado correctamente.')

    except Exception as e:
        conn.rollback()
        flash(f'Error al guardar el artículo: {str(e)}')
        raise

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('entidades.articulos'))



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

    # Artículo
    cursor.execute(
        'SELECT * FROM articulos WHERE id = %s',
        (id,)
    )
    articulos = cursor.fetchall()

    # Rubros
    cursor.execute(
        'SELECT * FROM articulos_rubros ORDER BY concepto'
    )
    rubros = cursor.fetchall()

    # Proveedores
    cursor.execute(
        'SELECT * FROM proveedores ORDER BY concepto'
    )
    proveedores = cursor.fetchall()

    # Marcas
    cursor.execute(
        'SELECT * FROM articulos_marcas ORDER BY concepto'
    )
    marcas = cursor.fetchall()

    # Unidades
    cursor.execute(
        'SELECT * FROM articulos_unidades ORDER BY concepto'
    )
    unidades = cursor.fetchall()

    # Tipos de IVA
    cursor.execute(
        'SELECT * FROM articulos_tipos_iva ORDER BY concepto'
    )
    tiposiva = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'articulos/edit_articulo.html',
        articulos=articulos,
        rubros=rubros,
        proveedores=proveedores,
        marcas=marcas,
        unidades=unidades,
        tiposiva=tiposiva
    )


# Actualizar Articulo
@entidades_bp.route('/actualizar_articulo', methods=["POST"])
@login_required
def update():

    id = request.form.get('txtID')

    # Datos generales
    codigo = request.form.get('txtCodigo')
    codigoBarras = request.form.get('txtCodigoBarras')
    concepto = request.form.get('txtConcepto')
    descripcion = request.form.get('txtDescripcion')

    # Relaciones
    idrubro = request.form.get('txtRubro') or None
    idproveedor = request.form.get('txtProveedor') or None
    idmarca = request.form.get('txtMarca') or None
    idumedida = request.form.get('txtUnidad') or None
    idtipoiva = request.form.get('txtIVA') or None

    # Cantidades y precios
    puntoReposicion = request.form.get('txtPuntoReposicion') or None
    existencia = request.form.get('txtExistencia') or None
    dolar = request.form.get('txtDolar') or None
    precio = request.form.get('txtPrecio') or None
    precioCosto = request.form.get('txtPrecioCosto') or None

    # Ganancias y precios de venta
    porcentajeGanancia = request.form.get('txtPorcentajeGanancia') or None
    precontado = request.form.get('txtPrecioMinorista') or None
    porcentajeGananciaMayorista = request.form.get('txtPorcentajeGananciaMayorista') or None
    precioVentaMayorista = request.form.get('txtPrecioMayorista') or None

    # Fechas
    fechaVencimiento = request.form.get('txtFechaVencimiento') or None
    fechaUltimaCarga = request.form.get('txtFechaUltimaCarga') or None

    # Casillas
    activo = 1 if request.form.get('txtActivo') else 0
    oferta = 1 if request.form.get('txtOferta') else 0

    # Foto
    foto = request.files.get('txtFoto')
    nuevoNombreFoto = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Recuperar foto anterior
        cursor.execute(
            "SELECT foto FROM articulos WHERE id=%s",
            (id,)
        )
        fila = cursor.fetchone()

        # Si se seleccionó una foto nueva
        if foto and foto.filename != '':

            now = datetime.now()
            tiempo = now.strftime("%Y%m%d%H%M%S")
            nuevoNombreFoto = tiempo + foto.filename

            foto.save(
                os.path.join(
                    current_app.config['CARPETA'],
                    nuevoNombreFoto
                )
            )

        # Actualizar artículo
        sql = """
            UPDATE articulos SET
                codigo=%s,
                codigoBarras=%s,
                concepto=%s,
                descripcion=%s,
                idrubro=%s,
                idproveedor=%s,
                idmarca=%s,
                puntoReposicion=%s,
                existencia=%s,
                idumedida=%s,
                dolar=%s,
                precio=%s,
                idtipoiva=%s,
                precioCosto=%s,
                porcentajeGanancia=%s,
                precontado=%s,
                porcentajeGananciaMayorista=%s,
                precioVentaMayorista=%s,
                fechaVencimiento=%s,
                fechaUltimaCarga=%s,
                activo=%s,
                oferta=%s
        """

        datos = [
            codigo,
            codigoBarras,
            concepto,
            descripcion,
            idrubro,
            idproveedor,
            idmarca,
            puntoReposicion,
            existencia,
            idumedida,
            dolar,
            precio,
            idtipoiva,
            precioCosto,
            porcentajeGanancia,
            precontado,
            porcentajeGananciaMayorista,
            precioVentaMayorista,
            fechaVencimiento,
            fechaUltimaCarga,
            activo,
            oferta
        ]

        # Si hay foto nueva, también actualizarla
        if nuevoNombreFoto:
            sql += ", foto=%s"
            datos.append(nuevoNombreFoto)

        sql += " WHERE id=%s"
        datos.append(id)

        cursor.execute(sql, tuple(datos))
        conn.commit()

        # Borrar foto anterior solamente después de guardar
        if nuevoNombreFoto and fila and fila['foto']:

            ruta_foto = os.path.join(
                current_app.config['CARPETA'],
                fila['foto']
            )

            if os.path.exists(ruta_foto):
                os.remove(ruta_foto)

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('entidades.articulos'))




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

