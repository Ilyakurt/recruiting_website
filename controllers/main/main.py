# from asyncio import constants
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
# from ..auth import auth
from functools import wraps
from models import add_vacancy, posts

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/')
def main():
    print ('main session:', session)
    # search = False
    # q = request.args.get('q')
    # if q:
    #     search = True
    # page = request.args.get(get_page_parameter(), type=int, default=1)

    # users = User.find(...)
    # pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')
    
    with UseDatabase(current_app.config['db']['postgres']) as cursor:
        cursor.execute("""SELECT company, description, salary, name, id FROM vacancy""")
        schema = ['company', 'description', 'salary', 'name', 'id']
        result = []
        for con in cursor.fetchall():
            result.append(dict(zip(schema, con)))
        return render_template('main.html', result = result)

@main_blueprint.route('/posts/<int:id>', methods=['GET', 'POST'])
def button(id):
    if request.method == 'GET':
        model = posts.PostsModel('postgres')
        result = model.select_post(id)
        # with UseDatabase(current_app.config['db']['postgres']) as cursor:
        #     cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
        #     schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
        #     result = []
        #     for con in cursor.fetchall():
        #         result.append(dict(zip(schema, con)))
        return render_template('detail.html', result = result)
    if session:
        if request.method == 'POST':
            if 'response_button' in request.form:
                model = posts.PostsModel('postgres')
                user = session['user_id']
                result = model.otclick(id, user)
                print('kek_1', id, session['user'])
        return ('Ваше резюме успешно отправлено')
    else:
        return ('Вам нужно зарегистрироваться')

@main_blueprint.route('/new_vacancy', methods=['GET', 'POST'])
def new_vacancy():
    print (session)
    if session:
        if session['role'] == 'admin':
            if 'add_button' in request.form:
                company = session['comp_name']
                description = 'Краткое описание отсутствует'
                name = request.form['name']
                full_description = request.form['full_description']
                email = request.form['email']
                address = request.form['address']
                if (request.form['salary']):
                    salary = request.form['salary']
                else:
                    salary = 0
                print (company, description, name, full_description, salary, email, address)
                with UseDatabase(current_app.config['db']['postgres']) as cursor:
                    cursor.execute("""INSERT INTO vacancy(company, description, name, full_description, salary, email, address)
                    VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s')""" % (company, description, name, full_description, salary, email, address) )
                return render_template('vacancy.html', success = True)
            return render_template('vacancy.html')
        else:
            return "Нет доступа"
    else:
        return "Нет доступа"

@main_blueprint.route('/response')
def response():
    print ('response', session)
    model = add_vacancy.Vacancy('postgres')
    result_1 = model.select_response()
    print ('ff', result_1)
    return render_template('response.html', result_1 = result_1)
