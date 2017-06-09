import os
import flask
from flask import Flask
import flask_login

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.secret_key = os.urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo': {'pw': 'secret'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    users.is_authenticated = request.form['pw'] == users[email]['pw']
    return user


@app.route('/')
def hello():
    print('isinstance', isinstance(app.config, dict))
    for conf in app.config:
        print(conf, ':', app.config.get(conf))
    return app.config['MESSAGE']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='邮箱'></input>
                <input type='password' name='pw' id='pw' placeholder='密码'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))

if __name__ == '__main__':
    app.run()
