from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Banco de dados reiniciado com sucesso!")
