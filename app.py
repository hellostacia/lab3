from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к запрашиваемой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'


class User(UserMixin):
    def __init__(self, user_id, login, password):
        self.id = user_id
        self.login = login
        self.password = password


USERS = {'user': User('1', 'user', 'qwerty')}


@login_manager.user_loader
def load_user(user_id):
    for user in USERS.values():
        if user.id == user_id:
            return user
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/counter')
def counter():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('counter.html', visits=session['visits'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_value = request.form.get('login')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        user = USERS.get(login_value)
        if user and user.password == password:
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


if __name__ == '__main__':
    app.run(debug=True)
