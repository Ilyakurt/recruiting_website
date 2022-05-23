# from asyncio import constants
from pickle import GET
import re
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
from models import question

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

@quiz_blueprint.route('/create', methods=['GET', 'POST'])
def quiz_create():
    if session:
        if request.method == 'GET':
            user_id = session['user_id']
            model = question.Quiz('postgres')
            result = model.select_quiz(user_id)
            len_res = len(result)
            if len_res > 0:
                for i in range (len_res):
                    qid = result[i]['qid']
                    quiz_count = model.select_quiz_count(qid)
                    result[i]['count']  = quiz_count
            else:
                quiz_count = 0
            return render_template('create_quiz.html', result = result)
        if request.method == 'POST':
            if 'create_quiz' in request.form:
                print ("POST")
                user_id = session['user_id']
                model = question.Quiz('postgres')
                result = model.create_quiz(user_id)
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
            if lens > 0:
                if data_1[lens - 1]['qid'] == qid:
                    return render_template('quiz_edit.html', result = result, data_1 = data_1)
                else:
                    data_1.clear()
                    return render_template('quiz_edit.html', result = result, data_1 = data_1)
            else:
                return render_template('quiz_edit.html', result = result, data_1 = data_1)
        if request.method == 'POST':
            if 'question_add' in request.form:
                data = dict(request.form)                
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
            else:
                print (request.form)
                return redirect(url_for('quiz_blueprint.quiz'))
                
        else:
            return redirect(url_for('quiz_blueprint.quiz'))
    else:
        return redirect(url_for('quiz_blueprint.quiz')) 