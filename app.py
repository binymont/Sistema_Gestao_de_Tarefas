from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task, User
from datetime import datetime
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração de e-mail para desenvolvimento local
default_sender = 'no-reply@localhost'
app.config.update(
    MAIL_SERVER='localhost',
    MAIL_PORT=1025,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER=default_sender
)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

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

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='recover-salt')
            link = url_for('reset_password', token=token, _external=True)
            msg = Message('Recuperação de senha', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
            msg.body = f'Clique no link para redefinir sua senha:\n\n{link}'
            mail.send(msg)
        flash('Se o e-mail existir, você receberá instruções para redefinir a senha.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='recover-salt', max_age=3600)
    except:
        flash('Link inválido ou expirado.', 'error')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first_or_404()
        user.set_password(request.form['password'])
        db.session.commit()
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'error')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f'Olá, {username}! Fico feliz em saber que vc se cadastrou! 💖', 'success')
        return redirect(url_for('login'))
    flash('Bem-vindo(a)! Para acessar, faça seu cadastro.', 'info')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Hello baby: Seja bem-vindo ao Sistema de Gestão!', 'success')
            return redirect(url_for('index'))
        flash('Credenciais inválidas, tente novamente! 🙄💅', 'error')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Bye, Bye! Até breve! 😠', 'info')
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    Task.query.filter_by(user_id=current_user.id).delete()
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Conta excluída. Espero que volte! 💕', 'warning')
    return redirect(url_for('register'))

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
        'done': sum(1 for t in tasks if t.status == 'done')
    }
    return render_template('index.html', pending_tasks=pending_tasks, completed_tasks=completed_tasks, counts=counts, show_form=True, user=current_user)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    priority = request.form['priority']
    status = request.form.get('status', 'todo')
    new_task = Task(title=title, description=description, due_date=due_date, priority=priority, status=status, completed=(status=='done'), user_id=current_user.id)
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
    task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
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
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Foto de perfil atualizada com sucesso!', 'success')
    else:
        flash('Tipo de arquivo inválido. Envie uma imagem PNG, JPG ou GIF.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
