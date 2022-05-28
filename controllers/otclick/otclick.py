from flask import render_template, request, session, redirect, Blueprint, current_app, url_for, abort
from DBCM import UseDatabase
from models import add_vacancy, posts, users, vacancy, employer, resume, question, otclick

otclick_blueprint = Blueprint('otclick_blueprint', __name__, template_folder='templates')

@otclick_blueprint.route('/response')
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

@otclick_blueprint.route('/response/<int:id>', methods=['GET', 'POST'])
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
                    len_res = len(result)
                    for res in range(len_res):
                        qid = result[res]['qid']
                        if qid != None:
                            model = question.Quiz('postgres')
                            qid_count = int(model.select_quiz_count(qid))
                            count_right_answer = int(model.count_right_answer(user_id, qid))
                            result[res]['qid_count'] = qid_count
                            result[res]['count_right_answer'] = count_right_answer
                            percent = (round(count_right_answer * 100 / qid_count, 2)) 
                            result[res]['percent'] = percent
                        else:
                            pass
                    print (result)
                    return render_template('vacancy_otclick.html', result = result)
                else: 
                    return render_template('error_url.html')
            else: 
                return render_template('error_url.html')
        if request.method == 'POST':
            print ("aaaaaaaaaaa", request.form)
            model = otclick.OtclickModel('postgres')
            id_vac = id
            id_user = request.form['id_user']
            resume_id = request.form['resume_id']
            if 'think' in request.form:
                status = 2
                result = model.status_update(status, id_vac, id_user, resume_id)
                return redirect(url_for('main_blueprint.response_resume', id = id))
            if 'invite' in request.form:
                status = 3
                result = model.status_update(status, id_vac, id_user, resume_id)
                return redirect(url_for('main_blueprint.response_resume', id = id))
            if 'rejection' in request.form:
                status = 4
                result = model.status_update(status, id_vac, id_user, resume_id)
                return redirect(url_for('main_blueprint.response_resume', id = id))
            return redirect(url_for('main_blueprint.main'))
    return redirect(url_for('main_blueprint.main'))