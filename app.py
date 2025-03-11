from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
from datetime import datetime
import os  # Importando o módulo 'os' para acessar variáveis de ambiente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    tasks = Task.query.all()
    show_form = True  # Controla se o formulário de cadastro será exibido ou não
    return render_template('index.html', tasks=tasks, show_form=show_form)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date_str = request.form['due_date']
    priority = request.form['priority']

    # Converter a string da data para o formato Python datetime.date
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

    # Criar uma nova tarefa
    new_task = Task(title=title, description=description, due_date=due_date, priority=priority)
    db.session.add(new_task)
    db.session.commit()

    # Redireciona para a página inicial para ver a lista atualizada
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.title = request.form['title']
    task.description = request.form['description']
    due_date_str = request.form['due_date']
    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    task.priority = request.form['priority']
    db.session.commit()
    return redirect(url_for('task_detail', task_id=task.id))

if __name__ == '__main__':
    # Configurando o Flask para escutar no PORT fornecido pelo Heroku
    port = int(os.environ.get('PORT', 5000))  # Pega a variável de ambiente 'PORT', ou usa 5000 se não estiver definida
    app.run(host='0.0.0.0', port=port, debug=True)  # O host deve ser '0.0.0.0' para aceitar conexões externas
