# from asyncio import constants
from pickle import GET
import re
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
from models import question

quiz_blueprint = Blueprint('quiz_blueprint', __name__, template_folder='templates')

@quiz_blueprint.route('')
def quiz():
    model = question.Quiz()
    result = model.get_subject()
    return render_template('quiz.html', result = result)

@quiz_blueprint.route('/<int:qid>', methods=['GET', 'POST'])
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
                result = model.quiz_id(qid)
                for res in result:
                    val = list(res.values())
                    val1 = str(val[0])
                    answer = request.form[val1]
                    print (answer)
                return ('Тест завершен')
        else:
            return ('Требуется войти в систему')
