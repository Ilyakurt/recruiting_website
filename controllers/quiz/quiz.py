# from asyncio import constants
from pickle import GET
import re
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
from models import question, posts, users

quiz_blueprint = Blueprint('quiz_blueprint', __name__, template_folder='templates')

@quiz_blueprint.route('')
def quiz():
    return render_template('quiz_menu.html')

@quiz_blueprint.route('/list')
def quiz_menu():
    model = question.Quiz('postgres')
    result = model.get_subject()
    return render_template('quiz.html', result = result)

@quiz_blueprint.route('/list/<int:qid>', methods=['GET', 'POST'])
def quiz_button(qid):
    if request.method == 'GET':
        model = question.Quiz('postgres')
        result = model.select_description(qid)
        return render_template('quiz_detail.html', result = result)
    if request.method == 'POST':
        if session:
            if 'quiz' in request.form:
                model = question.Quiz('postgres')
                result = model.quiz_question(qid)
                return render_template('quiz_test.html', result = result)
            if 'quiz_end' in request.form:
                model = question.Quiz('postgres')
                # result = model.quiz_id(qid)
                data = request.form.to_dict()
                del data['quiz_end']
                # for res in result:
                #     val = list(res.values())
                #     val1 = str(val[0])
                #     answer = request.form[val1]
                #     print (answer)
                for question_id, answer in data.items():
                    model = question.Quiz('postgres')
                    result = model.user_result_insert(qid, question_id, answer, 1, session['user_id'])

                return ('Тест завершен')
        else:
            return redirect(url_for('main_blueprint.main'))

@quiz_blueprint.route('/list/<int:qid>/<int:vac_id>/<int:resume_id>', methods=['GET', 'POST'])
def quiz_vacancy(qid, vac_id, resume_id):
    if request.method == 'GET':
        model = question.Quiz('postgres')
        result = model.select_description(qid)
        return render_template('quiz_detail.html', result = result)
    if request.method == 'POST':
        if session:
            if 'quiz' in request.form:
                model = question.Quiz('postgres')
                result = model.quiz_question(qid)
                return render_template('quiz_test.html', result = result)
            if 'quiz_end' in request.form:
                model = question.Quiz('postgres')
                data = request.form.to_dict()
                del data['quiz_end']
                for question_id, answer in data.items():
                    model = question.Quiz('postgres')
                    result = model.user_result_insert(qid, question_id, answer, 1, session['user_id'])
                post_model = posts.PostsModel('postgres')
                result_otclick = post_model.otclick_quiz(vac_id, session['user_id'], resume_id, qid)
                return redirect(url_for('main_blueprint.main'))
        else:
            return redirect(url_for('main_blueprint.main'))

@quiz_blueprint.route('/create', methods=['GET', 'POST'])
def quiz_create():
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = question.Quiz('postgres')
            model_user = users.UsersModel('postgres')
            check = model_user.employer_check()
            result = model.select_quiz(user_id)
            len_res = len(result)
            if len_res > 0:
                for i in range (len_res):
                    qid = result[i]['qid']
                    quiz_count = model.select_quiz_count(qid)
                    result[i]['count']  = quiz_count
            else:
                quiz_count = 0
            return render_template('create_quiz.html', check = check, result = result)
        if request.method == 'POST':
            if 'create_quiz' in request.form:
                print ("POST")
                user_id = session['user_id']
                model = question.Quiz('postgres')
                result = model.create_quiz(user_id)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            if 'delete_quiz' in request.form:
                qid = request.form['delete_quiz']
                model = question.Quiz('postgres')
                result = model.delete_quiz(qid)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            if 'check_resume' in request.form:
                qid = request.form['check_resume']
                model = question.Quiz('postgres')
                status = 5 
                result = model.update_status(qid, status)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            if 'cancellation' in request.form:
                qid = request.form['cancellation']
                model = question.Quiz('postgres')
                status = 0
                result = model.update_status(qid, status)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            if 'publish' in request.form:
                qid = request.form['publish']
                model = question.Quiz('postgres')
                status = 2
                result = model.update_status(qid, status)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            if 'invisible' in request.form:
                qid = request.form['invisible']
                model = question.Quiz('postgres')
                status = 3
                result = model.update_status(qid, status)
                return redirect(url_for('quiz_blueprint.quiz_create'))
    else:
        return redirect(url_for('quiz_blueprint.quiz'))

@quiz_blueprint.route('/edit/<int:qid>', methods=['GET', 'POST'])
def quiz_edit(qid, data_1 = []):
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = question.Quiz('postgres')
            result = model.select_quiz_edit(user_id, qid)
            lens = len(data_1)
            print (lens)
            if lens > 0:
                if data_1[lens - 1]['qid'] == qid:
                    print ("1")
                    return render_template('quiz_edit.html', result = result, data_1 = data_1)
                else:
                    print ("2")
                    data_1.clear()
                    data_1 = model.quiz_question(qid)
                    return redirect(url_for('quiz_blueprint.quiz_edit', qid = qid,  data_1 = data_1))
            if lens == 0:
                data = model.quiz_question(qid)
                if len(data) > 0:
                    for i in range(len(data)):
                        data_1.append(data[i])
                        len_data = len(data_1)
                        data_1[len_data - 1]['question_num'] = len_data
                    return redirect(url_for('quiz_blueprint.quiz_edit', qid = qid,  data_1 = data_1))
                else:
                    return render_template('quiz_edit.html', result = result, data_1 = data_1)
        if request.method == 'POST':
            if 'question_add' in request.form:
                question_str = str(request.form['question'])    
                check = int(request.form['check'])   
                option1 = str(request.form['option1'])   
                option2 = str(request.form['option2'])  
                option3 = str(request.form['option3'])    
                option4 = str(request.form['option4'])   
                data = {'question': question_str, 'check': check, 'option1': option1, 'option2': option2, 'option3': option3, 'option4': option4}     
                data_1.append(data)
                user_id = session['user_id']
                model = question.Quiz('postgres')
                result = model.select_quiz_edit(user_id, qid)
                len_data = len(data_1)
                data_1[len_data - 1]['question_num'] = len_data
                data_1[len_data - 1]['qid'] = qid
                return redirect(url_for('quiz_blueprint.quiz_edit', qid = qid,  data_1 = data_1))
            if 'delete_question' in request.form:
                len_data = len(data_1)
                del_data = int(request.form['delete_question'])
                del data_1[del_data - 1]
                for i in range (del_data - 1, len_data - 1):
                    data_1[i]['question_num'] = i + 1
                return redirect(url_for('quiz_blueprint.quiz_edit', qid = qid,  data_1 = data_1))
            if 'edit_subject' in request.form:
                subject = request.form['subject']
                description = request.form['description']
                model = question.Quiz('postgres')
                num_quiz = model.edit_quiz(subject, description, qid)
                return redirect(url_for('quiz_blueprint.quiz_edit', qid = qid,  data_1 = data_1))
            if 'save_quiz' in request.form:
                model = question.Quiz('postgres')
                delete_queistion = model.delete_quiz_question(qid)
                for res in data_1:
                    question_str = str(res['question'])
                    option1 = str(res['option1'])
                    option2 = str(res['option2'])
                    option3 = str(res['option3'])
                    option4 = str(res['option4'])
                    check = int(res['check'])
                    qid_edit = model.update_quiz_question(question_str, option1, option2, option3, option4, check, qid)
                return redirect(url_for('quiz_blueprint.quiz_create'))
            else:
                return render_template('error_url.html')
                
        else:
            return render_template('error_url.html')
    else:
        return render_template('error_url.html')

@quiz_blueprint.route('/quiz/pass', methods=['GET', 'POST'])
def quiz_user_pass(qid,):
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = question.Quiz('postgres')
            result = model.quiz_pass(user_id, qid)
    else:
        return render_template('error_url.html')

@quiz_blueprint.route('/check', methods=['GET', 'POST'])
def quiz_check():
    if session:
        if session['role'] == 'metodist':
            if request.method == 'GET':
                model = question.Quiz('postgres')
                result = model.quiz_check()
                print (result)
                return render_template('quiz_check.html', result = result)
            if request.method == 'POST':
                if 'approve' in request.form:
                    qid = request.form['qid']
                    model = question.Quiz('postgres')
                    status = 1
                    result = model.update_status(qid, status)
                    return redirect(url_for('quiz_blueprint.quiz_check'))
                if 'modification' in request.form:
                    qid = request.form['qid']
                    model = question.Quiz('postgres')
                    status = 4
                    result = model.update_status(qid, status)
                    return redirect(url_for('quiz_blueprint.quiz_check'))

        return render_template('error_url.html')
    return render_template('error_url.html')

@quiz_blueprint.route('/check/<int:qid>', methods=['GET', 'POST'])
def check_quiz_question(qid):
    if session:
        if session['role'] == 'metodist':
            if request.method == 'GET':
                model = question.Quiz('postgres')
                result = model.quiz_description(qid)
                data_1 = model.quiz_question(qid)
                print (result)
                return render_template('quiz_question.html', result = result, data_1 = data_1)
            if request.method == 'POST':
                if 'approve' in request.form:
                    qid = request.form['qid']
                    model = question.Quiz('postgres')
                    status = 1
                    result = model.update_status(qid, status)
                    return redirect(url_for('quiz_blueprint.quiz_check'))
                if 'modification' in request.form:
                    qid = request.form['qid']
                    model = question.Quiz('postgres')
                    status = 4
                    result = model.update_status(qid, status)
                    return redirect(url_for('quiz_blueprint.quiz_check'))
        return render_template('error_url.html')
    return render_template('error_url.html')