from flask import Flask, request, redirect, url_for, render_template, g, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, \
    login_user, login_required, logout_user
from sqlalchemy import text, extract
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import func

from functools import wraps
from datetime import date


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


# models
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


class Attendance(db.Model):
    __tablename__ = 'attendance'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    day = db.Column(db.DateTime, primary_key=True)

    def __str__(self):
        return '%r' % self.day


class Allowance(db.Model):
    __tablename__ = 'allowance'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    day = db.Column(db.DateTime, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    bounty = db.Column(db.Integer)

    def __str__(self):
        return '%r--%r' % (self.day, self.bounty)


class Salary(db.Model):
    __tablename__ = 'salary'
    uid = db.Column(db.Integer, db.ForeignKey('info.uid'), primary_key=True)
    dept = db.Column(db.String(40))
    month = db.Column(db.DateTime, primary_key=True)
    salary = db.Column(db.Integer)

    def __str__(self):
        return str(self.salary)


@app.cli.command('initdb')
def initdb_command():
    print('Start init, {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    with app.open_resource('schema.sql', mode='r') as f:
        db.engine.execute(text(f.read()).execution_options(autocommit=True))
    print('Initialized the database')


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('admin.login'))


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_admin:
            return redirect(url_for('admin.denied'))
        return func(*args, **kw)
    return wrapper


@app.route('/')
def index():
    return redirect(url_for('admin.index'))


# views
class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('index.html')

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
                try:
                    u = User(int(uid), pw, name, email, job, dept)
                    db.session.add(u)
                    db.session.commit()
                    flash("注册成功，您的工号是{}，姓名是{}".format(uid, name))
                    return redirect(url_for('admin.index'))
                except Exception as e:
                    print(e)
                    error = '注册失败，请检查您输入的是否正确'
        jts = [job.type for job in Job.query.all()]
        return self.render('signup.html', error=error, jts=jts)

    @expose("/logout")
    @login_required
    def logout(self):
        logout_user()
        flash('注销成功')
        return redirect(url_for('admin.index'))

    @expose('/denied')
    def denied(self):
        return self.render('denied.html')


class InfoView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        A = db.session.query(func.sum(Salary.salary)).\
            filter(Salary.uid==current_user.uid, extract('year', Salary.month)==2017).scalar() or 0
        B = db.session.query(func.sum(Allowance.bounty)).\
            filter(Allowance.uid==current_user.uid, extract('year', Allowance.day)==2017).scalar() or 0
        # A = sum(slr.salary for slr in current_user.salaries
        #         if slr.month.year == 2017)
        # B = sum(alw.bounty for alw in current_user.allowances
        #         if alw.day.year == 2017)
        return self.render('info.html', yeb=(A+B)//12)


class PersonalView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated

    def get_query(self):
        # return self.model.query.filter_by(uid=current_user.uid)
        return self.session.query(self.model).filter(self.model.uid==current_user.uid)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.uid==current_user.uid)


class ManageView(ModelView):
    can_export = True
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class ManageJob(ManageView):
    form_columns = ['type', 'rank', 'base_salary']


class ManageUser(ManageView):
    column_searchable_list = ['uid', 'name', 'email', 'job', 'dept']
    column_list = ['uid', 'name', 'email', 'job', 'dept', 'is_admin']
    form_columns = ['uid', 'pw', 'name', 'email', 'job', 'dept', 'is_admin']


class ManageAttendance(ManageView):
    column_searchable_list = ['uid']
    form_columns = ['uid', 'day']

    def on_model_change(self, form, model, is_created):
        model.day = model.day.date()
        return model


class ManageAllowance(ManageView):
    column_searchable_list = ['uid', 'day']
    form_columns = ['uid', 'day', 'hour', 'type']

    def on_model_change(self, form, model, is_created):
        model.day = model.day.date()
        model.bounty = (100, 70, 60, 50, 40)[model.type] * model.hour
        return model


class ManageSalary(ManageView):
    column_searchable_list = ['uid', 'month', 'dept']
    form_columns = ['uid', 'month']

    def on_model_change(self, form, model, is_created=True):
        model.month = date(model.month.year, model.month.month, 1)
        user = User.query.get(model.uid)
        basic = user._job.base_salary
        atd_days = db.session.query(func.count('*')).\
            filter(Attendance.uid == model.uid,
                   extract('year', Attendance.day) == extract('year', model.month),
                   extract('month', Attendance.day) == extract('month', model.month),
                   ).scalar() or 0
        alw_sum = sum(alw.bounty for alw in user.allowances
                      if (alw.day.year, alw.day.month) == (model.month.year, model.month.month))
        model.salary = basic + atd_days*100 + alw_sum
        model.dept = user.dept
        return model


admin = Admin(app, name='工资管理系统', index_view=HomeView(name='主页'))
admin.add_view(InfoView(name='个人信息', url='info'))
admin.add_view(PersonalView(Attendance, db.session, name='个人考勤'))
admin.add_view(PersonalView(Allowance, db.session, name='个人津贴'))
admin.add_view(PersonalView(Salary, db.session, name='个人工资'))
admin.add_view(ManageJob(Job, db.session, name='工种', category='数据管理', endpoint='mgjob'))
admin.add_view(ManageUser(User, db.session, name='员工', category='数据管理', endpoint='mguser'))
admin.add_view(ManageAttendance(Attendance, db.session, name='考勤', category='数据管理', endpoint='mgatd'))
admin.add_view(ManageAllowance(Allowance, db.session, name='津贴', category='数据管理', endpoint='mgalw'))
admin.add_view(ManageSalary(Salary, db.session, name='工资', category='数据管理', endpoint='mgslr'))
