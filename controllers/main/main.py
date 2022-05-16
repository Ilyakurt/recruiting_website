# from asyncio import constants
from sre_constants import SUCCESS
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
# from ..auth import auth
from functools import wraps
from models import add_vacancy, posts, users, vacancy, employer, resume

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/', methods=['GET', 'POST'])
def main():
    page = request.args.get('page', 1, type = int)
    first_page = (page-1)*15
    if request.method == 'GET': 
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT company, description, salary, name, id 
                FROM vacancy
                LIMIT 15
                OFFSET %s
                """ % (first_page))
            schema = ['company', 'description', 'salary', 'name', 'id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return render_template('main.html', result = result)
    if request.method == 'POST':
        if 'search_button' in request.form:
            name = request.form['search']
            model = posts.PostsModel('postgres')
            result = model.search_vacancy(name)
            return render_template('main.html', result = result, name = name)
        else:
            return ("X")
    else:
        redirect(url_for('main_blueprint.main'))

@main_blueprint.route('/page=2', methods=['GET', 'POST'])
def pagination():
    if request.method == 'GET':
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""SELECT company, description, salary, name, id 
            FROM vacancy
            LIMIT 15
            OFFSET 0
            """)
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
        if session:
            if session['role'] == 'client':
                user_id = session['user_id']
                model = resume.ResumeModel('postgres')
                user_resume = model.select_resume(user_id)
                print (resume)
                return render_template('detail.html', result = result, user_resume = user_resume)
            return render_template('detail.html', result = result)
        return render_template('detail.html', result = result)
    if session:
        if request.method == 'POST':
            print ("post")
            print (request.form)
            if 'send_resume' in request.form:
                model = posts.PostsModel('postgres')
                user = session['user_id']
                resume_id = request.form['resume_id']
                model.otclick(id, user, resume_id)
                result = model.select_post(id)
            return render_template('detail.html', result = result, success=True)
    else:
        return ('Вам нужно зарегистрироваться')

@main_blueprint.route('/employer_profile/<company>', methods=['GET', 'POST'])
def employer_profile(company):
    if request.method == 'GET':
        model = employer.EmployerModel('postgres')
        result = model.employer_company_profile(company)
        if len(result) > 0:
            return render_template('employer_company_profle.html', result = result) 
        else:
            return render_template('employer_company_profle.html') 

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
    model = add_vacancy.Vacancy('postgres')
    result_1 = model.select_response()
    return render_template('response.html', result_1 = result_1)

@main_blueprint.route('/vacancy', methods=['GET', 'POST'])
def profile_vacancy():
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = vacancy.VacancyModel('postgres')
            result = model.user_vacancy(user_id)
            return render_template('profile_vacancy.html', result = result)
        if request.method == 'POST':
            if 'save_change' in request.form:
                data = request.form
                vac_salary = request.form['salary']
                vac_status = request.form['active']
                vac_id = request.form['id']
                model = vacancy.VacancyModel('postgres')
                result = model.user_vacancy_status_salary_update(vac_id, vac_status, vac_salary)
                print ("data is is", data)
                return redirect(url_for('main_blueprint.profile_vacancy'))
    else:
        return redirect(url_for('main_blueprint.main'))

@main_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if session:
        if request.method == 'GET':
            if session['role'] == 'client':
                user = session['user_id']
                print(user)
                model = users.UsersModel('postgres')
                result = model.profile(user)
                if len(result) == 0:
                    user_id = model.profile_create(user)
                    result = model.profile(user_id)
                    return render_template('profile.html', result = result)
                else:
                    return render_template('profile.html', result = result)
            else:
                user = session['user_id']
                model = users.UsersModel('postgres')
                result = model.profile_employer(user)
                print ('res', result)
                return render_template('profile.html', result = result)
        if request.method == 'POST':
            if 'new_number' in request.form:
                phone_number = request.form['phone_number']
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.phone_number_update(phone_number, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_region' in request.form:
                region = request.form['region']
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.region_update(region, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_email' in request.form:
                email = request.form['email']
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.email_update(email, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_name' in request.form:
                name = request.form['name']
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.name_update(name, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_last_name' in request.form:
                last_name = request.form['last_name']
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.last_name_update(last_name, user_id)
                return redirect(url_for('main_blueprint.profile'))
        else:
            return "AAA?"
    else:
        return redirect(url_for('main_blueprint.main'))

