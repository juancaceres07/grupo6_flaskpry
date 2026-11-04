import os
from app import app, db, appbuilder

if os.path.exists("app.db"):
    os.remove("app.db")

with app.app_context():
    db.create_all()
    appbuilder.sm.create_db()
    role_admin = appbuilder.sm.find_role('Admin')
    
    user = appbuilder.sm.find_user(username='admin')
    if not user:
        appbuilder.sm.add_user(
            username='admin',
            first_name='Juan',
            last_name='Caceres',
            email='admin@fab.org',
            role=role_admin,
            password='admin'
        )
        print(">>> USUARIO CREADO CON ÉXITO: admin / admin <<<")
    else:
        appbuilder.sm.reset_password(user.id, 'admin')
        print(">>> CONTRASEÑA RESETEADA A: admin <<<")
