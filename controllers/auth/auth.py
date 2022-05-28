from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from models import users
from DBCM import UseDatabase
from functools import wraps
# from logger import logger, log_decorator

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')
logout_blueprint = Blueprint('logout_blueprint', __name__)


@auth_blueprint.route('/auth', methods=['GET', 'POST'])
def authorization():
    print (session)
    if 'login_button' in request.form:
        result = []
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            try:
                with UseDatabase(current_app.config['db']['postgres']) as cursor:
                    cursor.execute ("""
                        SELECT role, user_id
                        FROM users
                        WHERE login='%s' AND password='%s'
                        """ % (login, password))
                    schema = ['role', 'user_id']
                    for con in cursor.fetchall():
                        result.append(dict(zip(schema, con)))
            except:
                return redirect(url_for('auth_blueprint.authorization'))
            if len(result) > 0:
                session['role'] = result[0]['role']
                session['user_id'] = result[0]['user_id']
                session['user'] = login
                if result[0]['role'] == 'employer':
                    model = users.UsersModel('postgres')
                    company = model.company_employer(result[0]['user_id'])
                    session['company'] = str(company[1:-1])
                print (session)
                return redirect(url_for('main_blueprint.main'))
            else:
                return render_template('auth.html', status='bad')
        else:
            return render_template('auth.html', status='bad')
    elif 'registration_button' in request.form:
        return render_template('user_create.html', user_data={}, already_exists=False)
    elif 'registration_employer_button' in request.form:
        return render_template('employer_create.html', user_data={}, already_exists=False)
    elif 'save_new_user' in request.form:
        data = request.form
        if data['password'] == data['repeat_password']:
            role = 'client'
            exists, user_data = create_new_user(data, role)
            print (exists, user_data)
            if not exists:
                #logger.info(session['name'] + " создал нового пользователя")
                model = users.UsersModel('postgres')
                model.profile_create(user_data)
                return render_template('auth.html', new_user_login=data['login'])
            else:
                return render_template('user_create.html', user_data=user_data, already_exists=True)
        else:
            return render_template('user_create.html', mismatched_passwords=True, new_user_login=data['login'])
    elif 'save_new_employer' in request.form:
        data = request.form
        # create_new_employer(data)
        if data['password'] == data['repeat_password']:
            role = 'employer'
            exists, user_data = create_new_user(data, role)
            if not exists:
                model = users.UsersModel('postgres')
                user_company = data.get("company")
                status = 0
                try:
                    comp = model.insert_company(user_company, status)
                except:
                    status = 2
                create_new_employer(data, user_data, status)
                model.profile_create(user_data)
                user_company = data.get("company")
                return render_template('auth.html', new_user_login=data['login'])
            else:
                print (data)
                return render_template('employer_create.html', user_data=user_data, already_exists=True, data=data)
        else:
            return render_template('employer_create.html', mismatched_passwords=True, data=data)
    else:
        return render_template('auth.html')


def create_new_user(data, role):
    model = users.UsersModel('postgres')
    user_login = data.get("login")
    user_password = data.get("password")
    user_role = role
    created = model.insert_users(user_login, user_password, user_role)
    if created == 'None':
        return True, {'login': user_login,
                      'password': user_password,
                      'role': user_role}
    else:
        return False, created

# def create_new_employer_insert(data, role):
#     model = users.UsersModel('postgres')
#     user_login = data.get("login")
#     user_password = data.get("password")
#     user_role = role
#     created = model.insert_employer_to_users(user_login, user_password, user_role)
#     if created == 'None':
#         return True, {'login': user_login,
#                       'password': user_password,
#                       'role': user_role}
#     else:
#         return False, created

def create_new_employer(data, user_id, status):
    model = users.UsersModel('postgres')
    data = request.form
    user_name = data.get("name")
    user_last_name = data.get("last_name")
    user_company = data.get("company")
    user_phone = data.get("phone")
    user_email = data.get("email")
    user_city = data.get("city")
    user_address = data.get("address")
    user_id = user_id
    created = model.insert_employer(user_name, user_last_name, user_company, user_phone, user_email, user_city, user_address, user_id, status)
    print ("Был создан user_id", created)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth_blueprint.authorization'))
        return f(*args, **kwargs)
    return decorated_function

@logout_blueprint.route('/', methods=['GET', 'POST'])
def logout():
    # logger.info(session['name'] + " вышел из системы")
    if session['role'] == 'employer':
        session.pop('role')
        session.pop('user_id')
        session.pop('user')
        session.pop('company')
    else:
        session.pop('role')
        session.pop('user_id')
        session.pop('user')  
         
    return redirect(url_for('auth_blueprint.authorization'))