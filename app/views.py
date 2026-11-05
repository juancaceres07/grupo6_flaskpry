from flask import render_template, request
from flask_appbuilder import ModelView, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func
from . import appbuilder, db
from .models import Especie, Dueno, Mascota, Veterinario, CitaMedica, HistorialClinico

# --- VISTAS CRUD DE TABLAS ---
# En cada vista se define:
#   - list_columns:   columnas que se ven en el listado
#   - show_columns:   campos del detalle de un registro
#   - add/edit_columns: campos (y su orden) en los formularios
#   - search_columns: campos disponibles en el buscador
#   - label_columns:  nombres en español que ve el usuario
#   - base_order:     orden por defecto del listado

class EspecieView(ModelView):
    datamodel = SQLAInterface(Especie)

    list_title = "Especies"
    show_title = "Detalle de la especie"
    add_title = "Nueva especie"
    edit_title = "Editar especie"

    list_columns = ["nombre"]
    show_columns = ["nombre"]
    add_columns = ["nombre"]
    edit_columns = ["nombre"]
    search_columns = ["nombre"]
    label_columns = {"nombre": "Nombre"}
    base_order = ("nombre", "asc")


class DuenoView(ModelView):
    datamodel = SQLAInterface(Dueno)

    list_title = "Dueños"
    show_title = "Detalle del dueño"
    add_title = "Nuevo dueño"
    edit_title = "Editar dueño"

    list_columns = ["nombre", "telefono", "email", "direccion"]
    show_columns = ["nombre", "telefono", "email", "direccion"]
    add_columns = ["nombre", "telefono", "email", "direccion"]
    edit_columns = ["nombre", "telefono", "email", "direccion"]
    search_columns = ["nombre", "telefono", "email"]
    label_columns = {
        "nombre": "Nombre completo",
        "telefono": "Teléfono",
        "email": "Correo electrónico",
        "direccion": "Dirección",
    }
    base_order = ("nombre", "asc")


class MascotaView(ModelView):
    datamodel = SQLAInterface(Mascota)

    list_title = "Mascotas"
    show_title = "Detalle de la mascota"
    add_title = "Nueva mascota"
    edit_title = "Editar mascota"

    list_columns = ["nombre", "especie", "dueno", "edad", "peso"]
    show_columns = ["nombre", "especie", "dueno", "edad", "peso"]
    add_columns = ["nombre", "especie", "dueno", "edad", "peso"]
    edit_columns = ["nombre", "especie", "dueno", "edad", "peso"]
    search_columns = ["nombre", "especie", "dueno"]
    label_columns = {
        "nombre": "Nombre",
        "especie": "Especie",
        "dueno": "Dueño",
        "edad": "Edad (años)",
        "peso": "Peso (kg)",
    }
    base_order = ("nombre", "asc")


class VeterinarioView(ModelView):
    datamodel = SQLAInterface(Veterinario)

    list_title = "Veterinarios"
    show_title = "Detalle del veterinario"
    add_title = "Nuevo veterinario"
    edit_title = "Editar veterinario"

    list_columns = ["nombre", "especialidad", "telefono"]
    show_columns = ["nombre", "especialidad", "telefono"]
    add_columns = ["nombre", "especialidad", "telefono"]
    edit_columns = ["nombre", "especialidad", "telefono"]
    search_columns = ["nombre", "especialidad"]
    label_columns = {
        "nombre": "Nombre",
        "especialidad": "Especialidad",
        "telefono": "Teléfono",
    }
    base_order = ("nombre", "asc")


class CitaMedicaView(ModelView):
    datamodel = SQLAInterface(CitaMedica)

    list_title = "Citas médicas"
    show_title = "Detalle de la cita"
    add_title = "Nueva cita"
    edit_title = "Editar cita"

    list_columns = ["fecha", "mascota", "veterinario", "motivo", "estado"]
    show_columns = ["fecha", "mascota", "veterinario", "motivo", "estado"]
    add_columns = ["fecha", "mascota", "veterinario", "motivo", "estado"]
    edit_columns = ["fecha", "mascota", "veterinario", "motivo", "estado"]
    search_columns = ["fecha", "mascota", "veterinario", "estado", "motivo"]
    label_columns = {
        "fecha": "Fecha",
        "mascota": "Mascota",
        "veterinario": "Veterinario",
        "motivo": "Motivo",
        "estado": "Estado",
    }
    # Las citas más recientes primero
    base_order = ("fecha", "desc")


class HistorialClinicoView(ModelView):
    datamodel = SQLAInterface(HistorialClinico)

    list_title = "Historiales clínicos"
    show_title = "Detalle del historial clínico"
    add_title = "Nuevo historial clínico"
    edit_title = "Editar historial clínico"

    list_columns = ["cita", "cita.mascota", "diagnostico", "tratamiento"]
    show_columns = ["cita", "cita.mascota", "cita.veterinario", "diagnostico", "tratamiento"]
    add_columns = ["cita", "diagnostico", "tratamiento"]
    edit_columns = ["cita", "diagnostico", "tratamiento"]
    search_columns = ["cita", "diagnostico", "tratamiento"]
    label_columns = {
        "cita": "Cita",
        "cita.mascota": "Mascota",
        "cita.veterinario": "Veterinario",
        "diagnostico": "Diagnóstico",
        "tratamiento": "Tratamiento",
    }

# --- VISTA DE REPORTES ANALÍTICOS ---
class ReportesView(BaseView):
    default_view = 'citas_por_veterinario'

    @expose('/citas-veterinario/')
    @has_access
    def citas_por_veterinario(self):
        datos = db.session.query(
            Veterinario.nombre, 
            func.count(CitaMedica.id)
        ).join(CitaMedica).group_by(Veterinario.id).all()
        
        return self.render_template('reporte.html', 
                                   titulo="Reporte 1: Citas por Veterinario", 
                                   headers=["Veterinario", "Total Citas"], 
                                   filas=datos)

    @expose('/mascotas-especie/')
    @has_access
    def mascotas_por_especie(self):
        datos = db.session.query(
            Especie.nombre, 
            func.count(Mascota.id)
        ).join(Mascota).group_by(Especie.id).all()
        
        return self.render_template('reporte.html', 
                                   titulo="Reporte 2: Mascotas por Especie", 
                                   headers=["Especie", "Total Mascotas"], 
                                   filas=datos)

    @expose('/citas-estado/')
    @has_access
    def citas_por_estado(self):
        datos = db.session.query(
            CitaMedica.estado, 
            func.count(CitaMedica.id)
        ).group_by(CitaMedica.estado).all()
        
        return self.render_template('reporte.html', 
                                   titulo="Reporte 3: Citas por Estado", 
                                   headers=["Estado", "Total"], 
                                   filas=datos)

# --- VISTA DEL ASISTENTE IA ---
class AsistenteIAView(BaseView):
    default_view = 'asistente'

    @expose('/asistente/', methods=['GET', 'POST'])
    @has_access
    def asistente(self):
        respuesta = None
        if request.method == 'POST':
            consulta = request.form.get('consulta')
            respuesta = f"Recomendación Clínica IA para '{consulta}': Se sugiere evaluar signos vitales, mantener hidratación constante y realizar exámen de sangre preventivo."
        
        return self.render_template('asistente_ia.html', respuesta=respuesta)

# --- REGISTROS EN EL MENÚ ---
appbuilder.add_view(EspecieView, "Especies", category="Gestión Veterinaria")
appbuilder.add_view(DuenoView, "Dueños", category="Gestión Veterinaria")
appbuilder.add_view(MascotaView, "Mascotas", category="Gestión Veterinaria")
appbuilder.add_view(VeterinarioView, "Veterinarios", category="Gestión Veterinaria")
appbuilder.add_view(CitaMedicaView, "Citas Médicas", category="Gestión Veterinaria")
appbuilder.add_view(HistorialClinicoView, "Historiales Clínicos", category="Gestión Veterinaria")

# Menú de Reportes Analíticos
appbuilder.add_view_no_menu(ReportesView)
appbuilder.add_link("Citas por Veterinario", href="/reportesview/citas-veterinario/", category="Reportes Analíticos")
appbuilder.add_link("Mascotas por Especie", href="/reportesview/mascotas-especie/", category="Reportes Analíticos")
appbuilder.add_link("Citas por Estado", href="/reportesview/citas-estado/", category="Reportes Analíticos")

# Menú del Asistente IA
appbuilder.add_view_no_menu(AsistenteIAView)
appbuilder.add_link("Asistente IA", href="/asistenteiaview/asistente/", category="Asistente IA")