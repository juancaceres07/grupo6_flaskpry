from app import app, db
from app.models import Especie, Dueno, Mascota, Veterinario, CitaMedica, HistorialClinico

with app.app_context():
    metadata = Especie.metadata
    engine = db.engine
    for tabla in metadata.sorted_tables:
        print("--", tabla.name)

    metadata.create_all(bind=engine)
    print("creado correctamente")