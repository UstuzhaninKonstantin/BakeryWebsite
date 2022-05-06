from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from data import db_session
from data.users import User
from forms.buy import BuyForm
from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


CITIES = ['Москва', 'Казань', 'Санкт-Петербург', 'Пермь', 'Киров',
          'Белая Холуница', 'Ижевск', 'Воронеж', 'Уфа', 'Челябинск', 'Краснодар']
PRICES = {
        'beliy_hleb': ['Белый хлеб', 45],
        'cheburek': ['Чебурек с мясом', 180],
        'cherniy_hleb': ['Черный хлеб', 45],
        'djokonda': ['Пирожное "Джоконда"', 199],
        'echpochmak': ['Эчпочмак', 99],
        'izum': ['Пирожок с изюмом', 29],
        'kapusta': ['Пирожок с капустой', 29],
        'kruassan': ['Круассан', 69],
        'kulich': ['Кулич', 199],
        'napoleon': ['Торт "Наполеон"', 499],
        'pizza': ['Мини-пицца', 49],
        'ponchik': ['Пончик', 49],
        'samsa': ['Самса', 49],
        'sosiska': ['Сосиска в тесте', 29],
        'vatrushka': ['Ватрушка', 15]
    }


def main():
    db_session.global_init("db/bakery.db")
    app.run(debug=True)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/comments")
def comments():
    return render_template("comments.html")


@app.route('/card_information/<product>/<cost>', methods=['GET', 'POST'])
def card_info(product, cost):
    global PRICES, CITIES
    rus_product = PRICES[product][0]
    form = BuyForm()
    if form.validate_on_submit():
        if form.city.data not in CITIES:
            error = 'Нет доставки в ваш город'
            back = '/card_information/' + product + '/' + cost
            return render_template('error.html', error=error, back=back)
        for element in form:
            print(element)
        return redirect('/thanks_for_buying')
    return render_template('card_info.html', product=rus_product, cost=cost, form=form)


@app.route('/thanks_for_buying')
def thanks_for_buying():
    return render_template('thanks_for_buying.html')


@app.route("/buy/<product>")
@login_required
def buy_product(product):
    global PRICES
    string = '/static/img/' + product + '.png'
    path2 = '/card_information/' + product + '/' + str(PRICES[product][1])
    print(path2)
    return render_template('buy.html', product=product, info=PRICES, path=string, path2=path2)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('error.html',
                               error="Неправильный логин или пароль",
                               back='/login')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('error.html', error="Пароли не совпадают", back='/register')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('error.html', error="Такой пользователь уже есть", back='/register')
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


if __name__ == '__main__':
    main()
