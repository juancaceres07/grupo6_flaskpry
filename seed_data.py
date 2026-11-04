from datetime import datetime, timedelta
from app import app, db
from app.models import Especie, Dueno, Mascota, Veterinario, CitaMedica, HistorialClinico

with app.app_context():
    print("Cargando datos de prueba...")

    # 1. Especies
    canino = Especie(nombre="Canino")
    felino = Especie(nombre="Felino")
    ave = Especie(nombre="Ave")
    db.session.add_all([canino, felino, ave])
    db.session.commit()

    # 2. Dueños
    d1 = Dueno(nombre="Carlos Mendoza", telefono="71234567", email="carlos@gmail.com", direccion="Av. Las Américas 123")
    d2 = Dueno(nombre="Ana Gutiérrez", telefono="78901234", email="ana@gmail.com", direccion="Calle Bolivar 456")
    d3 = Dueno(nombre="Roberto Silva", telefono="65432109", email="roberto@gmail.com", direccion="Calle Sucre 789")
    db.session.add_all([d1, d2, d3])
    db.session.commit()

    # 3. Mascotas
    m1 = Mascota(nombre="Max", edad=3, peso=15.5, especie_id=canino.id, dueno_id=d1.id)
    m2 = Mascota(nombre="Luna", edad=2, peso=4.2, especie_id=felino.id, dueno_id=d2.id)
    m3 = Mascota(nombre="Rocky", edad=5, peso=22.0, especie_id=canino.id, dueno_id=d3.id)
    m4 = Mascota(nombre="Poli", edad=1, peso=0.3, especie_id=ave.id, dueno_id=d1.id)
    db.session.add_all([m1, m2, m3, m4])
    db.session.commit()

    # 4. Veterinarios
    v1 = Veterinario(nombre="Dr. Alejandro Torres", especialidad="Cirugía Veterinaria", telefono="70011223")
    v2 = Veterinario(nombre="Dra. Sofia Lopez", especialidad="Medicina General y Felinos", telefono="70044556")
    db.session.add_all([v1, v2])
    db.session.commit()

    # 5. Citas Médicas
    c1 = CitaMedica(fecha=datetime.now() - timedelta(days=2), motivo="Chequeo general y vacunas", estado="Completada", mascota_id=m1.id, veterinario_id=v1.id)
    c2 = CitaMedica(fecha=datetime.now() - timedelta(days=1), motivo="Fiebre y desparasitación", estado="Completada", mascota_id=m2.id, veterinario_id=v2.id)
    c3 = CitaMedica(fecha=datetime.now() + timedelta(days=1), motivo="Revisión de pata trasera", estado="Pendiente", mascota_id=m3.id, veterinario_id=v1.id)
    c4 = CitaMedica(fecha=datetime.now() + timedelta(days=3), motivo="Corte de pico y plumas", estado="Pendiente", mascota_id=m4.id, veterinario_id=v2.id)
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    # 6. Historiales Clínicos (Sin el campo fecha)
    h1 = HistorialClinico(diagnostico="Paciente saludable. Se aplica vacuna antirrábica.", tratamiento="Reposo 24 hrs.", mascota_id=m1.id)
    h2 = HistorialClinico(diagnostico="Infección estomacal leve.", tratamiento="Administrar antibiótico cada 12 hrs por 5 días.", mascota_id=m2.id)
    db.session.add_all([h1, h2])
    db.session.commit()

    print(">>> ¡DATOS DE PRUEBA CARGADOS CON ÉXITO! <<<")
