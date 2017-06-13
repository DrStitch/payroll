from flask import Flask, request, redirect, url_for, render_template, g, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import text
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


class Job(db.Model):
    __tablename__ = 'job'
    type = db.Column(db.String(40), primary_key=True)
    rank = db.Column(db.Integer)
    base_salary = db.Column(db.Integer)
    users = db.relationship('User', backref='_job')

    def __init__(self, type, rank, base_salary):
        self.type = type
        self.rank = rank
        self.base_salary = base_salary

    def __str__(self):
        return self.type

    def __repr__(self):
        return '<Job %r>' % self.type


class User(db.Model, UserMixin):
    __tablename__ = 'info'
    uid = db.Column(db.Integer, primary_key=True)
    pw = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    job = db.Column(db.String(40), db.ForeignKey('job.type'), nullable=False)
    dept = db.Column(db.String(40))
    is_admin = db.Column(db.Boolean, default=False)
    attendances = db.relationship('Attendance', backref='_user')
    allowances = db.relationship('Allowance', backref='_user')
    salaries = db.relationship('Salary', backref='_user')

    def __init__(self, uid, pw, name, email, job, dept):
        self.uid = uid
        self.pw = pw
        self.name = name
        self.email = email
        self.job = job
        self.dept = dept

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % self.name

    def get_id(self):
        return self.uid

    def is_authenticated(self):
        return self.is_admin


class Attendance(db.Model):
    __tablename__ = 'attendance'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    day = db.Column(db.DateTime, primary_key=True)


class Allowance(db.Model):
    __tablename__ = 'allowance'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    day = db.Column(db.DateTime, primary_key=True)
    hour = db.Column(db.Integer)
    type = db.Column(db.Integer)
    bounty = db.Column(db.Integer)


class Salary(db.Model):
    __tablename__ = 'salary'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    month = db.Column(db.DateTime, primary_key=True)
    salary = db.Column(db.Integer)


@app.cli.command('initdb')
def initdb_command():
    print('Start init, {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    with app.open_resource('schema.sql', mode='r') as f:
        db.engine.execute(text(f.read()).execution_options(autocommit=True))
    print('Initialized the database')


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


@app.route('/')
def index():
    return "欢迎使用工资管理系统"


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         uid = request.form['uid']
#         pw = request.form['pw']
#         if uid == '':
#             error = '工号不能为空'
#         elif pw == '':
#             error = '密码不能为空'
#         else:
#             user = User.query.filter_by(uid=int(uid), pw=pw).first()
#             if not user:
#                 error = '工号或密码错误'
#             else:
#                 login_user(user)
#                 flash('You were logged in')
#                 return redirect(url_for('index'))
#     return render_template('admin/login.html', error=error)


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     error = None
#     if request.method == 'POST':
#         uid = request.form['uid']
#         pw = request.form['pw']
#         name = request.form['name']
#         email = request.form['email']
#         job = request.form['job']
#         dept = request.form['dept']
#         if not (uid and pw and name and email and job and dept):
#             error = '信息不完整'
#         else:
#             try:
#                 u = User(int(uid), pw, name, email, job, dept)
#                 db.session.add(u)
#                 db.session.commit()
#                 flash("注册成功")
#                 return """
#                 <p>注册成功</p>
#                 <p>您的工号是{}，姓名是{}</p>
#                 """.format(uid, name)
#             except Exception as e:
#                 print(e)
#                 error = '注册失败，请检查您输入的是否正确'
#     return render_template('signup.html', error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('注销成功')
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('accountview.login'))


admin = Admin(app, name='工资管理系统')


class AccountView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('accountview.login'))

    @expose('login', methods=['GET', 'POST'])
    def login(self):
        error = None
        if request.method == 'POST':
            uid = request.form['uid']
            pw = request.form['pw']
            if uid == '':
                error = '工号不能为空'
            elif pw == '':
                error = '密码不能为空'
            else:
                user = User.query.filter_by(uid=int(uid), pw=pw).first()
                if not user:
                    error = '工号或密码错误'
                else:
                    login_user(user)
                    flash('You were logged in')
                    return redirect(url_for('infoview.index'))
        return self.render('login.html', error=error)

    @expose('signup', methods=['GET', 'POST'])
    def signup(self):
        pass


class InfoView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return "hahaha"


class AttendanceView(ModelView):
    pass


class ModelViewPK(ModelView):
    can_export = True
    column_display_pk = True


admin.add_view(AccountView(name='账户', url=''))
admin.add_view(InfoView(name='个人信息', url='info'))
admin.add_view(ModelViewPK(Job, db.session, name='工种', category='数据管理'))
admin.add_view(ModelViewPK(User, db.session, name='员工', category='数据管理'))
admin.add_view(ModelViewPK(Attendance, db.session, name='考勤', category='数据管理'))
admin.add_view(ModelViewPK(Allowance, db.session, name='津贴', category='数据管理'))
admin.add_view(ModelViewPK(Salary, db.session, name='工资', category='数据管理'))