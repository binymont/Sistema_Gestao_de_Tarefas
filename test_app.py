import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
from app import app, db, Task
from datetime import datetime

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_task(self):
        response = self.client.post('/add', data={
            'title': 'Estudar Python',
            'description': 'Revisar unittest e flask',
            'due_date': '2025-04-10',
            'priority': 'Alta',
            'status': 'todo'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = Task.query.first()
            print(f"✔️ [CADASTRO] Tarefa salva com título: {task.title}")
            self.assertIsNotNone(task)
            self.assertEqual(task.title, 'Estudar Python')
        print("✅ Teste de CADASTRO passou com sucesso!")

    def test_edit_task(self):
        with app.app_context():
            task = Task(title='Tarefa Antiga', description='Desc.', due_date=datetime.today(), priority='Média')
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = self.client.post(f'/update/{task_id}', data={
            'title': 'Tarefa Editada',
            'description': 'Nova desc.',
            'due_date': '2025-04-20',
            'priority': 'Alta',
            'status': 'todo'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = Task.query.get(task_id)
            print(f"✔️ [EDIÇÃO] Tarefa após edição: {task.title}")
            self.assertEqual(task.title, 'Tarefa Editada')
        print("✅ Teste de EDIÇÃO passou com sucesso!")

    def test_delete_task(self):
        with app.app_context():
            task = Task(title='Tarefa para excluir', due_date=datetime.today(), priority='Baixa')
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = self.client.get(f'/delete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            task = Task.query.get(task_id)
            print(f"✔️ [EXCLUSÃO] Tarefa encontrada após exclusão: {task}")
            self.assertIsNone(task)
        print("✅ Teste de EXCLUSÃO passou com sucesso!")

    def test_toggle_complete(self):
        with app.app_context():
            task = Task(title='Completar tarefa', due_date=datetime.today(), priority='Média', completed=False)
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = self.client.post(f'/toggle_complete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            task = Task.query.get(task_id)
            print(f"✔️ [CONCLUSÃO] Status atual da tarefa: {'Concluída' if task.completed else 'Pendente'}")
            self.assertTrue(task.completed)
        print("✅ Teste de CONCLUSÃO passou com sucesso!")

if __name__ == '__main__':
    unittest.main()