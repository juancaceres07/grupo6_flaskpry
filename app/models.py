from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship

class Especie(Model):
    __tablename__ = 'especies'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.nombre

class Dueno(Model):
    __tablename__ = 'duenos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(200))

    def __repr__(self):
        return f"{self.nombre} ({self.telefono})"

class Mascota(Model):
    __tablename__ = 'mascotas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    edad = Column(Integer)
    peso = Column(Float)
    especie_id = Column(Integer, ForeignKey('especies.id'), nullable=False)
    especie = relationship("Especie")
    dueno_id = Column(Integer, ForeignKey('duenos.id'), nullable=False)
    dueno = relationship("Dueno")

    def __repr__(self):
        return self.nombre

class Veterinario(Model):
    __tablename__ = 'veterinarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    telefono = Column(String(20))

    def __repr__(self):
        return f"Dr(a). {self.nombre}"

class CitaMedica(Model):
    __tablename__ = 'citas_medicas'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    motivo = Column(String(200), nullable=False)
    estado = Column(String(20), default="Pendiente") # Pendiente, Completada, Cancelada
    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)
    mascota = relationship("Mascota")
    veterinario_id = Column(Integer, ForeignKey('veterinarios.id'), nullable=False)
    veterinario = relationship("Veterinario")

    def __repr__(self):
        return f"Cita #{self.id} - {self.fecha}"

class HistorialClinico(Model):
    __tablename__ = 'historiales_clinicos'
    id = Column(Integer, primary_key=True)
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=False)
    cita_id = Column(Integer, ForeignKey('citas_medicas.id'), nullable=False)
    cita = relationship("CitaMedica")

    def __repr__(self):
        return f"Historial Cita #{self.cita_id}"