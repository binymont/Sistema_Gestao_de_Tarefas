from app import app, db

# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()
