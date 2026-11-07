from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db_connection
from ges_seguridad.routes_seguridad import login_required
import os
from flask import send_file
from datetime import datetime
from flask import current_app
import subprocess

soporte_bp = Blueprint('soporte', __name__)

# Rubros
@soporte_bp.route('/rubros/rubros')
@login_required
def rubros():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos_rubros order by concepto;")
    rubros=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('rubros/rubros.html',rubros=rubros)


# Create Rubro
@soporte_bp.route('/create_rubro')
@login_required
def create_rubro():
    return render_template('rubros/rubro_create.html')

@soporte_bp.route('/guardar_rubro', methods=['POST'])
@login_required
def guardar_rubro():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_rubro'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos_rubros (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.rubros'))


# Eliminar Rubro
@soporte_bp.route('/destroy_rubro/<id>')
@login_required
def destroy_rubro(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos_rubros WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/rubros/rubros')

# Editar rubro
@soporte_bp.route('/edit_rubro/<id>')
@login_required
def edit_rubro(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos_rubros WHERE id = %s', (id,))
    rubros=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('rubros/rubro_edit.html', rubros=rubros)

# Actualizar Rubro
@soporte_bp.route('/actualizar_rubro', methods=["POST"])
@login_required
def actualizar_rubro():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE articulos_rubros
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.rubros'))


# Grupos
@soporte_bp.route('/grupos/grupos')
@login_required
def grupos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos_grupos order by concepto;")
    grupos=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('grupos/grupos.html',grupos=grupos)


# Create Grupo
@soporte_bp.route('/create_grupo')
@login_required
def create_grupo():
    return render_template('grupos/grupo_create.html')

@soporte_bp.route('/guardar_grupo', methods=['POST'])
@login_required
def guardar_grupo():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_grupo'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos_grupos (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.grupos'))


# Eliminar Grupo
@soporte_bp.route('/destroy_grupo/<id>')
@login_required
def destroy_grupo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos_grupos WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/grupos/grupos')

# Editar grupo
@soporte_bp.route('/edit_grupo/<id>')
@login_required
def edit_grupo(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos_grupos WHERE id = %s', (id,))
    grupos=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('grupos/grupo_edit.html', grupos=grupos)

# Actualizar Grupo
@soporte_bp.route('/actualizar_grupo', methods=["POST"])
@login_required
def actualizar_grupo():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE articulos_grupos
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.grupos'))




# Unidades
@soporte_bp.route('/unidades/unidades')
@login_required
def unidades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos_unidades order by concepto;")
    unidades=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('unidades/unidades.html',unidades=unidades)


# Create Unidad
@soporte_bp.route('/create_unidad')
@login_required
def create_unidad():
    return render_template('unidades/unidad_create.html')

@soporte_bp.route('/guardar_unidad', methods=['POST'])
@login_required
def guardar_unidad():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_unidad'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos_unidades (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.unidades'))


# Eliminar UNidad
@soporte_bp.route('/destroy_unidad/<id>')
@login_required
def destroy_unidad(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos_unidades WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/unidades/unidades')

# Editar Unidades
@soporte_bp.route('/edit_unidad/<id>')
@login_required
def edit_unidad(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos_unidades WHERE id = %s', (id,))
    unidades=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('unidades/unidad_edit.html', unidades=unidades)

# Actualizar Unidad
@soporte_bp.route('/actualizar_unidad', methods=["POST"])
@login_required
def actualizar_unidad():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE articulos_unidades
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.unidades'))



# Marcas
@soporte_bp.route('/marcas/marcas')
@login_required
def marcas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos_marcas order by concepto;")
    marcas=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('marcas/marcas.html',marcas=marcas)


# Create Marca
@soporte_bp.route('/create_marca')
@login_required
def create_marca():
    return render_template('marcas/marca_create.html')

@soporte_bp.route('/guardar_marca', methods=['POST'])
@login_required
def guardar_marca():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_marca'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos_marcas (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.marcas'))


# Eliminar Marca
@soporte_bp.route('/destroy_marca/<id>')
@login_required
def destroy_marca(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos_marcas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/marcas/marcas')

# Editar Marca
@soporte_bp.route('/edit_marca/<id>')
@login_required
def edit_marca(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos_marcas WHERE id = %s', (id,))
    marcas=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('marcas/marca_edit.html', marcas=marcas)

# Actualizar Marca
@soporte_bp.route('/actualizar_marca', methods=["POST"])
@login_required
def actualizar_marca():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE articulos_marcas
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.marcas'))



# Tipos_Iva
@soporte_bp.route('/tipos_iva')
@login_required
def tipos_iva():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articulos_tipos_iva order by concepto;")
    tiposiva=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('tipos_iva/tipos_iva.html',tiposiva=tiposiva)

# Create Tipos_Iva
@soporte_bp.route('/create_tipo_iva')
@login_required
def create_tipo_iva():
    return render_template('tipos_iva/tipos_iva_create.html')

# Guardar Tipos_Iva
@soporte_bp.route('/guardar_tipo_iva', methods=['POST'])
@login_required
def guardar_tipo_iva():
    _concepto = request.form['txtConcepto']
    _alicuota = request.form['txtAlicuota']

    if _concepto == '' or _alicuota == 0:
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_tipo_iva'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO articulos_tipos_iva (concepto, alicuota, activo)
        VALUES (%s, %s, 1)
    """
    cursor.execute(sql, (_concepto, _alicuota))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_iva'))


# Eliminar Tipos_Iva
@soporte_bp.route('/destroy_tipo_iva/<id>')
@login_required
def destroy_tipo_iva(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM articulos_tipos_iva WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_iva'))

# Editar Tipos_Iva
@soporte_bp.route('/edit_tipo_iva/<id>')
@login_required
def edit_tipo_iva(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM articulos_tipos_iva WHERE id = %s', (id,))
    tiposiva=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('tipos_iva/tipos_iva_edit.html', tiposiva=tiposiva)

# Actualizar Tipos_Iva
@soporte_bp.route('/actualizar_tipo_iva', methods=["POST"])
@login_required
def actualizar_tipo_iva():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']
    _alicuota = request.form['txtAlicuota']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE articulos_tipos_iva
        SET concepto=%s,
            alicuota=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _alicuota, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_iva'))


# Localidades
@soporte_bp.route('/localidades')
@login_required
def localidades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM localidades order by concepto;")
    localidades=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('localidades/localidades.html',localidades=localidades)


# Create Localidad
@soporte_bp.route('/create_localidad')
@login_required
def create_localidad():
    return render_template('localidades/localidad_create.html')



@soporte_bp.route('/guardar_localidad', methods=['POST'])
@login_required
def guardar_localidad():
    _concepto = request.form['txtConcepto']
    _cp = request.form['txtcp']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_localidad'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO localidades (concepto, cp, idprovincia, activo)
        VALUES (%s, %s, 1, 1)
    """
    cursor.execute(sql, (_concepto,_cp))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.localidades'))


# Eliminar Localidad
@soporte_bp.route('/destroy_localidad/<id>')
@login_required
def destroy_localidad(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM localidades WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.localidades'))

# Editar Localidad
@soporte_bp.route('/edit_localidad/<id>')
@login_required
def edit_localidad(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM localidades WHERE id = %s', (id,))
    localidades=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('localidades/localidad_edit.html', localidades=localidades)

# Actualizar Localidades
@soporte_bp.route('/actualizar_localidad', methods=["POST"])
@login_required
def actualizar_localidad():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']
    _cp =request.form['txtcp']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE localidades
        SET concepto=%s,
            cp=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _cp, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.localidades'))


# Provincias
@soporte_bp.route('/provincias')
@login_required
def provincias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM provincias order by concepto;")
    provincias=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('provincias/provincias.html',provincias=provincias)


# Create Provincia
@soporte_bp.route('/create_provincia')
@login_required
def create_provincia():
    return render_template('provincias/provincia_create.html')

@soporte_bp.route('/guardar_provincia', methods=['POST'])
@login_required
def guardar_provincia():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_provincia'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO provincias (concepto, idpais, activo)
        VALUES (%s, 1, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.provincias'))

# Eliminar Provincia
@soporte_bp.route('/destroy_provincia/<id>')
@login_required
def destroy_provincia(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM provincias WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.provincias'))

# Editar Provincia
@soporte_bp.route('/edit_provincia/<id>')
@login_required
def edit_provincia(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM provincias WHERE id = %s', (id,))
    provincias=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('provincias/provincia_edit.html', provincias=provincias)

# Actualizar Provincia
@soporte_bp.route('/actualizar_provincia', methods=["POST"])
@login_required
def actualizar_provincia():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE provincias
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.provincias'))


# Paises
@soporte_bp.route('/paises')
@login_required
def paises():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paises order by concepto;")
    paises=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('paises/paises.html',paises=paises)


# Create Pais
@soporte_bp.route('/create_pais')
@login_required
def create_pais():
    return render_template('paises/pais_create.html')

@soporte_bp.route('/guardar_pais', methods=['POST'])
@login_required
def guardar_pais():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_pais'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO paises (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.paises'))


# Eliminar Pais
@soporte_bp.route('/destroy_pais/<id>')
@login_required
def destroy_pais(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM paises WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.paises'))

# Editar Pais
@soporte_bp.route('/edit_pais/<id>')
@login_required
def edit_pais(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM paises WHERE id = %s', (id,))
    paises=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('paises/pais_edit.html', paises=paises)

# Actualizar Pais
@soporte_bp.route('/actualizar_pais', methods=["POST"])
@login_required
def actualizar_pais():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE paises
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """

    datos = (_concepto, _activo, id)

    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.paises'))




# Tipos Contribuyente Fiscal
@soporte_bp.route('/tipos_contribuyente')
@login_required
def tipos_contribuyente():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipos_contribuyente order by concepto;")
    tiposContribuyente=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('tipos_contribuyente/tipos_contribuyente.html',tiposContribuyente=tiposContribuyente)


# Create Tipo Contribuyente
@soporte_bp.route('/create_tipos_contribuyente')
@login_required
def create_tipos_contribuyente():
    return render_template('tipos_contribuyente/tipos_contribuyente_create.html')

@soporte_bp.route('/guardar_tipos_contribuyente', methods=['POST'])
@login_required
def guardar_tipos_contribuyente():
    _concepto = request.form['txtConcepto']

    if _concepto == '':
        flash('Recuerda llenar todos los campos')
        return redirect(url_for('create_tipos_contribuyente'))

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO tipos_contribuyente (concepto, activo)
        VALUES (%s, 1)
    """
    cursor.execute(sql, (_concepto,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_contribuyente'))


# Eliminar Tipo Contribuyente
@soporte_bp.route('/destroy_tipos_contribuyente/<id>')
@login_required
def destroy_tipos_contribuyente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tipos_contribuyente WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_contribuyente'))

# Editar Tipo Contribuyente
@soporte_bp.route('/edit_tipos_contribuyente/<id>')
@login_required
def edit_tipos_contribuyente(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * FROM tipos_contribuyente WHERE id = %s', (id,))
    tiposContribuyente=cursor.fetchall()
    #conn.commit()

    cursor.close()
    conn.close()

    return render_template('tipos_contribuyente/tipos_contribuyente_edit.html', tiposContribuyente=tiposContribuyente)

# Actualizar Tipo Contribuyente
@soporte_bp.route('/actualizar_tipos_contribuyente', methods=["POST"])
@login_required
def actualizar_tipos_contribuyente():
    id = request.form['txtID']
    _concepto = request.form['txtConcepto']

    # Si el checkbox está marcado → vale 1
    # Si no viene en el form → vale 0
    _activo = 1 if 'txtActivo' in request.form else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE tipos_contribuyente
        SET concepto=%s,
            activo=%s
        WHERE id=%s
    """
    datos = (_concepto, _activo, id)
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('soporte.tipos_contribuyente'))

# =========================
# TABLA GENERAL
# =========================
@soporte_bp.route("/tablagral")
def tablagral():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM tablagral
        LIMIT 1
    """)

    empresa = cursor.fetchone()
    
     # LOCALIDADES
    cursor.execute("""
        SELECT
            id,
            concepto
        FROM localidades
        ORDER BY concepto
    """)

    localidades = cursor.fetchall()


    cursor.close()
    conn.close()

    return render_template(
        "tablagral.html",
        empresa=empresa,
        localidades=localidades
    )


# =========================
# ACTUALIZAR EMPRESA
# =========================
@soporte_bp.route(
    "/empresa_update",
    methods=["POST"]
)
def empresa_update():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE tablagral
            SET
                razonSocial=%s,
                nombreFantasia=%s,
                leyenda=%s,
                fechaInicioActividades=%s,
                direccion=%s,
                cp=%s,
                idlocali=%s,
                cuit=%s,
                ingresosBrutos=%s,
                telefono1=%s,
                telefono2=%s,
                mail=%s,
                sitioWeb=%s,
                redSocial=%s,
                redSocial2=%s,
                recargoTarjeta=%s,
                descuentoContado=%s,
                clienteRapido=%s

            LIMIT 1

        """, (

            request.form["txtRazonSocial"],
            request.form["txtNombreFantasia"],
            request.form["txtLeyenda"],
            request.form["txtFechaInicio"],
            request.form["txtDireccion"],
            request.form["txtCP"],
            request.form["txtIdLocali"],
            request.form["txtCuit"],
            request.form["txtIngresosBrutos"],
            request.form["txtTelefono1"],
            request.form["txtTelefono2"],
            request.form["txtMail"],
            request.form["txtSitioWeb"],
            request.form["txtRedSocial"],
            request.form["txtRedSocial2"],
            request.form["txtRecargoTarjeta"],
            request.form["txtDescuentoContado"],
            request.form["txtClienteRapido"]

        ))

                # =========================
        # LOGO
        # =========================
        archivo = request.files.get("txtLogo")

        if archivo and archivo.filename != "":

            extension = os.path.splitext(
                archivo.filename
            )[1].lower()

            # Solo permitir imágenes
            extensiones_permitidas = [".jpg", ".jpeg", ".png"]

            if extension not in extensiones_permitidas:
                raise Exception(
                    "Formato de logo no permitido. "
                    "Use JPG, JPEG o PNG."
                )

            # Nombre fijo para el logo
            nombre_logo = "logo" + extension

            ruta_img = os.path.join(
                current_app.root_path,
                "static",
                "img"
            )

            # Eliminar logos anteriores
            for ext in extensiones_permitidas:
                archivo_anterior = os.path.join(
                    ruta_img,
                    "logo" + ext
                )

                if os.path.exists(archivo_anterior):
                    os.remove(archivo_anterior)

            # Guardar nuevo logo
            ruta_logo = os.path.join(
                ruta_img,
                nombre_logo
            )

            archivo.save(ruta_logo)

        conn.commit()

        flash(
            "Datos actualizados correctamente",
            "success"
        )

    except Exception as e:

        conn.rollback()

        flash(
            f"Error: {str(e)}",
            "danger"
        )

    finally:

        cursor.close()
        conn.close()

    return redirect(
        url_for("soporte.tablagral")
    )
    



# =========================
# BACKUP BASE DATOS
# =========================
@soporte_bp.route("/backup_bd")
@login_required
def backup_bd():

    nombre = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    ruta = os.path.join(
        current_app.root_path,
        "backups",
        nombre
    )

    os.makedirs(
        os.path.dirname(ruta),
        exist_ok=True
    )

    mysqldump = r"C:\wamp64\bin\mysql\mysql9.1.0\bin\mysqldump.exe"

    with open(ruta, "w", encoding="utf-8") as archivo:
        subprocess.run(
            [
                mysqldump,
                "-u", "root",
                "--databases", "stiopticajch",
                "--routines",
                "--triggers",
                "--events"
            ],
            stdout=archivo,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

    return send_file(
        ruta,
        as_attachment=True
    )