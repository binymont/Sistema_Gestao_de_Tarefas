from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task, User
from datetime import datetime
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta_aqui'

# Upload de imagem de perfil
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'profile_pics')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Hello, faça login para continuar 🌸💖'
login_manager.login_message_category = 'info'

login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.template_filter('dateformat')
def dateformat(value, format='%Y-%m-%d'):
    return value.strftime(format)

@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    pending_tasks = [t for t in tasks if t.status != 'done']
    completed_tasks = [t for t in tasks if t.status == 'done']

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
        show_form=True,
        user=current_user
    )

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date_str = request.form['due_date']
    priority = request.form['priority']
    status = request.form.get('status', 'todo')

    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    completed = (status == 'done')

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status=status,
        completed=completed,
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    flash('Tarefa adicionada com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail_modal.html', task=task)

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)

    task.title = request.form['title']
    task.description = request.form['description']
    due_date_str = request.form['due_date']
    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    task.priority = request.form['priority']
    task.status = request.form['status']
    task.completed = (task.status == 'done')

    db.session.commit()
    flash('Tarefa atualizada com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle_complete/<int:id>', methods=['POST'])
@login_required
def toggle_complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    task.status = 'done' if task.completed else 'todo'
    db.session.commit()
    flash('Status da tarefa atualizado!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash(f'Olá, {username}! Fico feliz em saber que vc se cadastrou, acredito que esse sistema irá te ajudar muito com a administração das suas tarefas e fico muito feliz de saber que vou poder ter um pouquinho de participação nisso, faça bom proveito! 💖', 'success')
        return redirect(url_for('login'))
    else:
        flash('Bem-vindo(a) User <3\nPara acessar meu primeiro sistema disponibilizado online, vc precisa fazer o cadastro, ok baby?\nVamos lá!', 'info')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Hello baby: Seja bem-vindo ao Sistema de Gestão!', 'success')
            return redirect(url_for('index'))
        flash('PAROOU!, essas não são credênciais válidas, tenta dnv! 🙄💅', 'error')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Bye, Bye, te vejo em breve! Nos veremos em breve né? 😠', 'info')
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    Task.query.filter_by(user_id=current_user.id).delete()
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Fico muito triste em saber que vc excluiu a conta, mas vou te direcionar para a tela de registro. Espero que vc mude de ideia, Pequeno gafanhoto! heheh 💕', 'warning')
    return redirect(url_for('register'))

@app.route('/upload_profile_pic', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        flash('Nenhuma imagem enviada.', 'warning')
        return redirect(url_for('index'))

    file = request.files['profile_pic']

    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'warning')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{current_user.id}.png")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)
        flash('Foto de perfil atualizada com sucesso!', 'success')
    else:
        flash('Tipo de arquivo inválido. Envie uma imagem PNG, JPG ou GIF.', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
