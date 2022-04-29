from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from data import db_session
from data.users import User
from forms.add_comments import LeaveComment
from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/bakery.db")
    app.run(debug=True)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/buy/<product>")
@login_required
def del_job(product):
    return render_template('buy.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/task')
@login_required
def task():
    return render_template('tasks.html')


'''
@app.route("/news_delete/<int:id_job>")
@login_required
def del_job(id_job):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/index')


@app.route('/add_jobs', methods=['GET', 'POST'])
def add_jobs():
    form = AddJobs()
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.leader.data
        job.start_date = form.start.data
        job.end_date = form.end.data
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()
        return redirect('/index')
    return render_template('tasks.html', form=form)


@app.route('/news_edit/<int:id_job>', methods=['GET', 'POST'])
def edit_jobs(id_job):
    form = AddJobs()
    db_sess = db_session.create_session()
    jober = db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    if request.method == 'GET':
        form.job.data = jober.job
        form.work_size.data = jober.work_size
        form.collaborators.data = jober.collaborators
        form.leader.data = jober.team_leader
        form.start.data = jober.start_date
        form.end.data = jober.end_date

    if form.validate_on_submit():
        jober.job = form.job.data
        jober.work_size = form.work_size.data
        jober.collaborators = form.collaborators.data
        jober.team_leader = form.leader.data
        jober.start_date = form.start.data
        jober.end_date = form.end.data
        db_sess.commit()
        return redirect('/index')
    return render_template('tasks.html', form=form)


@app.route('/add/<header>/<content>/<id>/<int:private>')
@app.route('/add/<header>/<content>')
def news(header, content, private=0, id=1):
    db_sess = db_session.create_session()
    news = News()
    news.title = header
    news.content = content
    news.is_private = private
    news.user_id = id
    db_sess.add(news)
    db_sess.commit()
    return redirect('/')


'''

if __name__ == '__main__':
    main()
