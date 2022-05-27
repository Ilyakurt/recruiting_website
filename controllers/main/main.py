from flask import render_template, request, session, redirect, Blueprint, current_app, url_for, abort
from DBCM import UseDatabase
from models import add_vacancy, posts, users, vacancy, employer, resume, question, otclick

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
            return render_template('main.html', result = result, name = name, page_paginate = 0, vacancy_count = vacancy_count)
        if vacancy_count > 15:
            model = posts.PostsModel('postgres')
            result = model.search_vacancy(name, num_page)
            return render_template('main.html', result = result, name = name, page_paginate = 0, vacancy_count = vacancy_count)
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
                try:
                    qid = result[0]['qid']
                    model = question.Quiz('postgres')
                    test_result = model.select_description(qid) 
                    return render_template('detail.html', result = result, user_resume = user_resume, test_result = test_result)
                except:
                    return render_template('detail.html', result = result, user_resume = user_resume)
            return render_template('detail.html', result = result)
        else:
            return render_template('detail.html', result = result)
    if session:
        if request.method == 'POST':
            if 'send_resume' in request.form:
                model = posts.PostsModel('postgres')
                user = session['user_id']
                resume_id = request.form['resume_id']
                model.otclick(id, user, resume_id)
                result = model.select_post(id)
            if 'quiz_test' in request.form:
                qid = request.form['qid']
                resume_id = request.form['resume_id']
                vac_id = id
                print (request.form)
                return redirect(url_for('quiz_blueprint.quiz_vacancy', qid = qid, vac_id = vac_id, resume_id = resume_id))
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
        if session['role'] == 'employer':
            if request.method == 'GET':
                user_id = session['user_id']
                quiz_model = question.Quiz('postgres')
                quiz_res = quiz_model.quiz_attach(user_id)
                return render_template('vacancy.html', quiz_res = quiz_res)
            if request.method == 'POST':
                if 'add_button' in request.form:
                    company = session['company']
                    description = request.form['small_description']
                    name = request.form['name']
                    full_description = request.form['full_description']
                    email = request.form['email']
                    address = request.form['address']
                    user_id = session['user_id']
                    qid = request.form['quiz_select']
                    if int(qid) == 0:
                        qid = 'NULL'
                    status = 1
                    if (request.form['salary']):
                        salary = request.form['salary']
                    else:
                        salary = 0
                    with UseDatabase(current_app.config['db']['postgres']) as cursor:
                        cursor.execute("""INSERT INTO vacancy(company, description, name, full_description, salary, email, address, id_user, status, qid)
                        VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', %s)""" % (company, description, name, full_description, salary, email, address, user_id, status, qid))
                    return render_template('vacancy.html', success = True)
            return render_template('vacancy.html')
        else:
            return render_template('error_url.html')
    else:
        return render_template('error_url.html')

@main_blueprint.route('/response')
def response():
    if session:
        user_id = session['user_id']
        role = session['role']
        if request.method == 'GET':
            if role == 'employer' or role == 'admin':
                model = vacancy.VacancyModel('postgres')
                result = model.user_vacancy(user_id)
                otclick_model = otclick.OtclickModel('postgres')
                otclick_result = otclick_model.select_otclick(user_id)
                print (result)
                print (otclick_result)
                return render_template('response.html', result = result, otclick_result = otclick_result)
            if role == 'client':
                model = resume.ResumeModel('postgres')
                result = model.select_response(user_id)
                return render_template('user_otclick.html', result = result)
    return redirect(url_for('main_blueprint.main'))

@main_blueprint.route('/response/<int:id>')
def response_resume(id):
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            role = session['role']
            if role == 'employer' or role == 'admin':
                model = otclick.OtclickModel('postgres')
                check_result = model.check_user(user_id, id)
                if int(check_result) == 1:
                    result = model.vacancy_resume(id)
                    print (result)
                    return render_template('vacancy_otclick.html', result = result)
                else: 
                    return render_template('error_url.html')
            return render_template('error_url.html')
    return redirect(url_for('main_blueprint.main'))

@main_blueprint.route('/vacancy', methods=['GET', 'POST'])
def profile_vacancy():
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = vacancy.VacancyModel('postgres')
            result = model.user_vacancy(user_id)
            quiz_model = question.Quiz('postgres')
            quiz_res = quiz_model.quiz_attach(user_id)
            print (quiz_res)
            return render_template('profile_vacancy.html', result = result, quiz_res = quiz_res)
        if request.method == 'POST':
            if 'save_change' in request.form:
                data = request.form
                vac_salary = request.form['salary']
                vac_status = request.form['active']
                vac_id = request.form['id']
                qid = request.form['quiz_select']
                print ("qid is", qid)
                model = vacancy.VacancyModel('postgres')
                result = model.user_vacancy_status_salary_update(vac_id, vac_status, vac_salary)
                if int(qid) != 0:
                    status = 2
                    post_model = posts.PostsModel('posgres')
                    post_model.quiz_attach(vac_id, qid, status)
                if int(qid) == 0:
                    status = 0
                    qid = 'NULL'
                    post_model = posts.PostsModel('posgres')
                    post_model.quiz_attach(vac_id, qid, status)
                print ("data is is", data)
                return redirect(url_for('main_blueprint.profile_vacancy'))
            if 'change_description' in request.form:
                vac_id = request.form['id']
                user_id = session['user_id']
                print ("111111111", vac_id, user_id)
                return redirect(url_for('main_blueprint.vacancy_edit', vac_id = vac_id))
            if 'delete_vacancy' in request.form:
                vac_id = request.form['id']
                model = posts.PostsModel('postgres')
                result = model.delete_post(vac_id)
                return redirect(url_for('main_blueprint.profile_vacancy'))
    else:
        return redirect(url_for('main_blueprint.main'))


@main_blueprint.route('/vacancy/edit/<int:vac_id>', methods=['GET', 'POST'])
def vacancy_edit(vac_id):
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = posts.PostsModel('postgres')
            result = model.edit_post(vac_id, user_id)
            return render_template('vacancy_edit.html', result = result)
        if request.method == 'POST':
            if 'save_button' in request.form:
                user_id = session['user_id']
                description = request.form['small_description']
                name = request.form['name']
                full_description = request.form['full_description']
                email = request.form['email']
                address = request.form['address']
                user_id = session['user_id']
                if (request.form['salary']):
                    salary = request.form['salary']
                else:
                    salary = 0
                print (vac_id, user_id, name, salary, email, address)
                model = posts.PostsModel('postgres')
                result = model.save_edit_post(vac_id, user_id, description, name, full_description, salary, email, address)
                return redirect(url_for('main_blueprint.button', id = vac_id))
    else:
        return redirect(url_for('main_blueprint.main'))

@main_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if session:
        if request.method == 'GET':
            success = request.args.get('success', 'True')
            print (success)
            if session['role'] == 'client':
                user = session['user_id']
                model = users.UsersModel('postgres')
                result = model.profile(user)
                if len(result) == 0:
                    user_id = model.profile_create(user)
                    result = model.profile(user_id)
                    return render_template('profile.html', result = result, success = success)
                else:
                    return render_template('profile.html', result = result, success = success)
            else:
                user = session['user_id']
                model = users.UsersModel('postgres')
                result = model.profile_employer(user)
                print ('res', result)
                return render_template('profile.html', result = result)
        if request.method == 'POST':
            if 'new_number' in request.form:
                phone_number = request.form['phone_number']
                if len(phone_number) == 0:
                    return redirect(url_for('main_blueprint.profile', success = 'phone_is_null'))
                else:
                    try:
                        int(phone_number)
                    except:
                        return redirect(url_for('main_blueprint.profile', success = 'phone_is_not_int'))
                    user_id = session['user_id']
                    model = users.UsersModel('postgres')
                    result = model.phone_number_update(phone_number, user_id)
                    return redirect(url_for('main_blueprint.profile'))
            if 'new_region' in request.form:
                region = request.form['region']
                if len(region) == 0:
                    return redirect(url_for('main_blueprint.profile', success = 'region_is_null'))
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.region_update(region, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_email' in request.form:
                email = request.form['email']
                if len(email) == 0:
                    return redirect(url_for('main_blueprint.profile', success = 'email_is_null'))
                try:
                    email.index('@')
                except:
                    return redirect(url_for('main_blueprint.profile', success = 'email_error'))
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.email_update(email, user_id)
                return redirect(url_for('main_blueprint.profile'))
            if 'new_name' in request.form:
                name = request.form['name']
                if len(name) == 0:
                    return redirect(url_for('main_blueprint.profile', success = 'name_is_null'))                
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.name_update(name, user_id)
                return redirect(url_for('main_blueprint.profile'))         
            if 'new_last_name' in request.form:
                last_name = request.form['last_name']
                if len(last_name) == 0:
                    return redirect(url_for('main_blueprint.profile', success = 'last_name_is_null')) 
                user_id = session['user_id']
                model = users.UsersModel('postgres')
                result = model.last_name_update(last_name, user_id)
                return redirect(url_for('main_blueprint.profile'))
        else:
            return "AAA?"
    else:
        return redirect(url_for('main_blueprint.main'))

