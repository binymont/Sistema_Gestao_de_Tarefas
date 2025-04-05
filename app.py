from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Filtro customizado para formatar datas no template
@app.template_filter('dateformat')
def dateformat(value, format='%Y-%m-%d'):
    return value.strftime(format)

@app.route('/')
def index():
    tasks = Task.query.all()

    # Atualização: usa status para exibir concluídas
    pending_tasks = [t for t in tasks if t.status != 'done']
    completed_tasks = [t for t in tasks if t.status == 'done']

    # Contador por status para o dashboard
    counts = {
        'backlog': sum(1 for t in tasks if t.status == 'backlog'),
        'todo': sum(1 for t in tasks if t.status == 'todo'),
        'in_progress': sum(1 for t in tasks if t.status == 'in_progress'),
        'done': sum(1 for t in tasks if t.status == 'done'),
    }

    return render_template(
        'index.html',
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        counts=counts,
        show_form=True
    )

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date_str = request.form['due_date']
    priority = request.form['priority']
    status = request.form.get('status', 'todo')

    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    completed = (status == 'done')  # ← sincroniza

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status=status,
        completed=completed
    )
    db.session.add(new_task)
    db.session.commit()
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

@app.route('/update/<int:id>,', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)

    task.title = request.form['title']
    task.description = request.form['description']
    due_date_str = request.form['due_date']
    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    task.priority = request.form['priority']
    task.status = request.form['status']
    task.completed = (task.status == 'done')  # ← sincroniza ao editar

    db.session.commit()
    return redirect(url_for('task_detail', task_id=task.id))

@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    task.status = 'done' if task.completed else 'todo'  # ← sincroniza ao alternar
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
