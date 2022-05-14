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
    model = question.Quiz()
    result = model.get_subject()
    return render_template('quiz.html', result = result)

@quiz_blueprint.route('/list/<int:qid>', methods=['GET', 'POST'])
def quiz_button(qid):
    if request.method == 'GET':
        model = question.Quiz()
        result = model.select_description(qid)
        return render_template('quiz_detail.html', result = result)
    elif request.method == 'POST':
        if session:
            if 'quiz' in request.form:
                model = question.Quiz()
                result = model.quiz_question(qid)
                return render_template('quiz_test.html', result = result)
            if 'quiz_end' in request.form:
                model = question.Quiz()
                # result = model.quiz_id(qid)
                data = request.form.to_dict()
                del data['quiz_end']
                # for res in result:
                #     val = list(res.values())
                #     val1 = str(val[0])
                #     answer = request.form[val1]
                #     print (answer)
                for question_id, answer in data.items():
                    model = question.Quiz()
                    result = model.user_result_insert(qid, question_id, answer, 1, session['user_id'])

                return ('Тест завершен')
        else:
            return redirect(url_for('main_blueprint.main'))