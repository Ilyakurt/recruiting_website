from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
from models import add_vacancy, posts, users, vacancy, employer, resume

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/', methods=['GET', 'POST'])
def main():
    page = request.args.get('page', 1, type = int)
    num_page = (page - 1) * 15
    if request.method == 'GET':
        model = posts.PostsModel('postgres')
        page_paginate = int(model.count_vacancy()) // 15 + 1
        result = model.select_vacancy(num_page)
        return render_template('main.html', result = result, page_paginate = page_paginate)
    if request.method == 'POST':
        if 'search_button' in request.form:
            name = request.form['search']
            return redirect(url_for('main_blueprint.search_vacancy', search = name))

@main_blueprint.route('/search/<search>', methods=['GET', 'POST'])
def search_vacancy(search):
    if request.method == 'GET':
        name = search
        vacancy_model = posts.PostsModel('postgres')
        page = request.args.get('page', 1, type = int)
        num_page = (page - 1) * 15
        try:
            vacancy_count = int(vacancy_model.count_search_vacancy(name))
        except:
            return redirect(url_for('main_blueprint.main'))
        if vacancy_count > 0 and vacancy_count < 16:
            model = posts.PostsModel('postgres')
            result = model.search_vacancy(name, num_page)
            return render_template('main.html', result = result, name = name, page_paginate = 0)
        if vacancy_count > 15:
            model = posts.PostsModel('postgres')
            result = model.search_vacancy(name, num_page)
            return render_template('main.html', result = result, name = name, page_paginate = 0)
        else:
            return render_template('main.html', name = name, page_paginate = 0, search_count = 0)  
    if request.method == 'POST':
        if 'search_button' in request.form:
            name = request.form['search']
            return redirect(url_for('main_blueprint.search_vacancy', search = name))
        else:
            return redirect(url_for('main_blueprint.main'))
    else:
        return redirect(url_for('main_blueprint.main'))

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
    if session:
        print (session)
        user_id = session['user_id']
        role = session['role']
        if request.method == 'GET':
            if role == 'employer' or role == 'admin':
                print ("1")
                model = add_vacancy.Vacancy('postgres')
                result = model.select_response()
                return render_template('response.html', result = result)
            if role == 'client':
                print ("2")
                model = resume.ResumeModel('postgres')
                result = model.select_response(user_id)
                return render_template('user_otclick.html', result = result)
    return redirect(url_for('main_blueprint.main'))

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

