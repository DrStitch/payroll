import os
import psycopg2
from flask import Flask, request, redirect, url_for, render_template, g, flash
import flask_login


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def get_id(self):
        return self.uid

    @staticmethod
    def get(uid):
        db = get_db()
        cur = db.cursor()
        cur.execute("select name from info where uid=%s;", (uid, ))
        if cur.rowcount == 1:
            name = cur.fetchone()[0]
            return User(uid, name)
        return None

    @staticmethod
    def login(uid, pw):
        uid = int(uid)
        db = get_db()
        cur = db.cursor()
        cur.execute("select name from info where uid=%s and pass=%s", (uid, pw))
        if cur.rowcount == 1:
            name = cur.fetchone()[0]
            return User(uid, name)
        return None


def connect_db():
    conn = psycopg2.connect(app.config['DATABASE'])
    return conn


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    error and print(error)
    if hasattr(g, 'pg_db'):
        g.pg_db.close()


def init_db():
    """Initializes the database"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database')


@login_manager.user_loader
def load_user(uid):
    return User.get(uid)


@app.route('/')
def hello():
    return app.config['WELCOME']


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uid = request.form['uid']
        pw = request.form['pw']
        if uid == '':
            error = '工号不能为空'
        elif pw == '':
            error = '密码不能为空'
        else:
            user = User.login(uid, pw)
            if not user:
                error = '工号或密码错误'
            else:
                flask_login.login_user(user)
                flash('You were logged in')
                return redirect(url_for('hello'))
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        uid = request.form['uid']
        pw = request.form['pw']
        name = request.form['name']
        email = request.form['email']
        job = request.form['job']
        dept = request.form['dept']
        if not (uid and pw and name and email and job and dept):
            error = '信息不完整'
        else:
            uid = int(uid)
            db = get_db()
            cur = db.cursor()
            try:
                cur.execute('insert into info(uid, pass, name, email, job, dept) '
                            'values (%s, %s, %s, %s, %s, %s);', (uid, pw, name,
                                                                 email, job, dept))
                flash("注册成功")
                return """
                <p>注册成功</p>
                <p>您的工号是{}，姓名是{}</p>
                """.format(uid, name)
            except psycopg2.Error as e:
                error = e.pgerror
    return render_template('signup.html', error=error)


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash('注销成功')
    return redirect(url_for('hello'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
