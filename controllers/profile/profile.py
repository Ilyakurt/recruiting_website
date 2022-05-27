# from asyncio import constants
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
from models import resume, users

profile_blueprint = Blueprint('profile_blueprint', __name__, template_folder='templates')

@profile_blueprint.route('/applicant', methods=['GET', 'POST'])
def applicant():
    if session:
        if request.method == 'GET': 
            user_id = session['user_id']
            model = resume.ResumeModel('postgres')
            result = model.select_resume(user_id)
            return render_template('applicant_menu.html', result = result) 
        if request.method == 'POST':
            if 'create_resume' in request.form:
                user_id = session['user_id']
                model = resume.ResumeModel('postgres')
                result = model.create_resume(user_id)
                model.create_resume_experience(user_id, result)
                return redirect(url_for('profile_blueprint.applicant'))
            if 'delete_resume' in request.form:
                resume_id = request.form['delete_resume']
                user_id = session['user_id']
                model = resume.ResumeModel('postgres')
                model.delete_resume(user_id, resume_id)
                model.delete_resume_experience(user_id, resume_id)
                return redirect(url_for('profile_blueprint.applicant'))
            if 'active_resume' in request.form:
                user_id = session['user_id']
                resume_id = request.form['active_resume']
                model = resume.ResumeModel('postgres')
                model.active_resume(user_id, resume_id)
                return redirect(url_for('profile_blueprint.applicant'))
            if 'deactivation_resume' in request.form:
                user_id = session['user_id']
                resume_id = request.form['deactivation_resume']
                model = resume.ResumeModel('postgres')
                model.deactivation_resume(user_id, resume_id)
                return redirect(url_for('profile_blueprint.applicant'))
    else:
        return redirect(url_for('main_blueprint.profile'))

@profile_blueprint.route('/resume/<int:resume_id>', methods=['GET', 'POST'])
def resume_create(resume_id):
    if session:
        if request.method == 'GET':
            if session['role'] == 'client':
                if request.method == 'GET':
                    user_id = session['user_id']
                    model = resume.ResumeModel('postgres')
                    result = model.select_user(user_id)
                    user_resume = model.resume_edit(user_id, resume_id)
                    user_resume_experience = model.select_resume_experience(user_id, resume_id)
                    return render_template('resume.html', result = result, user_resume = user_resume, user_resume_experience = user_resume_experience)
            else:
                return redirect(url_for('main_blueprint.profile'))
    else:
        return redirect(url_for('main_blueprint.profile'))

@profile_blueprint.route('/resume/position/edit/<int:resume_id>', methods=['GET', 'POST'])
def user_position_edit(resume_id):
    if session:
        if session['role'] == 'client':
            if request.method == 'GET':
                print("Get")
                user_id = session['user_id']
                model = resume.ResumeModel('postgres')
                user_resume = model.resume_edit(user_id, resume_id)
                return render_template('position_edit.html', user_resume = user_resume)
            if request.method == 'POST':
                if 'save_button' in request.form:
                    print("Psot")
                    user_id = session['user_id']
                    position_work = request.form['position_work']
                    specialization = request.form['specialization']
                    salary = request.form['salary']
                    model = resume.ResumeModel('postgres')
                    user_resume = model.update_position(user_id, position_work, specialization, salary, resume_id)
                    print ("data is", position_work, specialization, salary)
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
                else:
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
            else:
                return redirect(url_for('main_blueprint.profile'))
    else:
        return redirect(url_for('main_blueprint.profile'))

@profile_blueprint.route('/resume/experience/edit/<int:resume_id>', methods=['GET', 'POST'])
def user_experience_edit(resume_id):
    if session:
        if session['role'] == 'client':
            if request.method == 'GET':
                user_id = session['user_id']
                model = resume.ResumeModel('postgres')
                select_resume_experience = model.select_resume_experience(user_id, resume_id)
                return render_template('experience_edit.html', select_resume_experience = select_resume_experience)
            if request.method == 'POST':
                if 'save_button' in request.form:
                    company = request.form['company']
                    position_work = request.form['position_work']
                    charge = request.form['charge']
                    region = request.form['region']
                    start_dttm = request.form['start_dttm']
                    if 'time' in request.form:
                        end_dttm = '2099-12-30'
                    else:
                        end_dttm = request.form['end_dttm']
                    user_id = session['user_id']
                    model = resume.ResumeModel('postgres')
                    model.update_experience(company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id)
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
                else:
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
        else:
            return redirect(url_for('main_blueprint.profile'))
    else:
        return redirect(url_for('main_blueprint.profile'))

@profile_blueprint.route('/resume/about/edit/<int:resume_id>', methods=['GET', 'POST'])
def user_about_edit(resume_id):
    if session:
        if session['role'] == 'client':
            if request.method == 'GET':
                    if request.method == 'GET':
                        user_id = session['user_id']
                        model = resume.ResumeModel('postgres')
                        user_resume = model.resume_edit(user_id, resume_id)
                        return render_template('about_edit.html', user_resume = user_resume)
            if request.method == 'POST':
                if 'save_button' in request.form:
                    user_id = session['user_id']
                    about = request.form['about']
                    model = resume.ResumeModel('postgres')
                    user_resume = model.update_about(user_id, about, resume_id)
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
                else:
                    return redirect(url_for('profile_blueprint.resume_create', resume_id = resume_id))
        else:
            return redirect(url_for('main_blueprint.profile'))
    else:
        return redirect(url_for('main_blueprint.profile'))

@profile_blueprint.route('/user/<int:id>/<int:vac_id>', methods=['GET', 'POST'])
def user_profile(id, vac_id):
    if session:
        if session['role'] == 'employer':
            if request.method == 'GET':
                user_id = id
                model = resume.ResumeModel('postgres')
                result = model.select_user(user_id)
                user_resume = model.resume_edit(user_id, vac_id)
                user_resume_experience = model.select_resume_experience(user_id, id)
                return render_template('user_profile.html', result = result, user_resume = user_resume, user_resume_experience = user_resume_experience)
                # model = employer.EmployerModel('postgres')
                # result = model.employer_company_profile(company)
                # if len(result) > 0:
                #     return render_template('employer_company_profle.html', result = result) 
                # else:
                #     return render_template('employer_company_profle.html') 
        return render_template('error_url.html')
    return render_template('error_url.html')

@profile_blueprint.route('/company_profile', methods=['GET', 'POST'])
def company_profile():
    if session:
        if session['role'] == 'employer':
            if request.method == 'GET':
                company = session['company']
                model = users.UsersModel('postgres')
                result = model.employer_company_profile(company)
                print (result)
                return render_template('company_profile.html', result = result)
            if request.method == 'POST':
                if 'description' in request.form:
                    company = session['company']
                    model = users.UsersModel('postgres')
                    result = model.employer_company_profile(company)
                    return render_template('company_profile.html', result = result, edit = True)
                if 'save_button' in request.form:
                    description = request.form['edit_description']
                    company = session['company']
                    print (company, description) 
                    model = users.UsersModel('postgres')
                    model.employer_company_profile_edit(company, description)
                    return redirect(url_for('profile_blueprint.company_profile'))
        else:
            return render_template('error_url.html')
    else:
        return render_template('error_url.html')