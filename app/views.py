from flask import current_app, render_template, request
from flask_appbuilder import ModelView, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.ai.asistente_ai import AsistenteAIError, obtener_respuesta
from sqlalchemy import func
from . import appbuilder, db
from .models import Especie, Dueno, Mascota, Veterinario, CitaMedica, HistorialClinico

# --- VISTAS CRUD DE TABLAS ---
class EspecieView(ModelView):
    datamodel = SQLAInterface(Especie)

class DuenoView(ModelView):
    datamodel = SQLAInterface(Dueno)

class MascotaView(ModelView):
    datamodel = SQLAInterface(Mascota)

class VeterinarioView(ModelView):
    datamodel = SQLAInterface(Veterinario)

class CitaMedicaView(ModelView):
    datamodel = SQLAInterface(CitaMedica)

class HistorialClinicoView(ModelView):
    datamodel = SQLAInterface(HistorialClinico)

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
        error = None
        consulta = ""

        if request.method == 'POST':
            consulta = request.form.get('consulta', '').strip()

            if not consulta:
                error = "Por favor, escribe una consulta."
            else:
                try:
                    respuesta = obtener_respuesta(consulta)
                except AsistenteAIError as exc:
                    error = exc.mensaje_usuario
                except Exception as exc:
                    # No registrar el texto de la excepción: el SDK puede incluir
                    # datos de la petición en sus detalles internos.
                    current_app.logger.error(
                        "Fallo interno en el asistente IA (%s)",
                        type(exc).__name__,
                    )
                    error = (
                        "No se pudo obtener una respuesta en este momento. "
                        "Intenta nuevamente."
                    )

        return self.render_template(
            'asistente_ia.html',
            consulta=consulta,
            respuesta=respuesta,
            error=error,
        )

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
