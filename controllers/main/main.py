# from asyncio import constants
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase
# from ..auth import auth
from functools import wraps
# from models import project

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/')
def main():
    print (session)
    with UseDatabase(current_app.config['db']['postgres']) as cursor:
        cursor.execute("""SELECT company, description, salary, name, id FROM vacancy""")
        schema = ['company', 'description', 'salary', 'name', 'id']
        result = []
        for con in cursor.fetchall():
            result.append(dict(zip(schema, con)))
        # return result
        return render_template('main.html', result = result)


@main_blueprint.route('/posts/<int:id>')
def button(id):
    print (session)
    with UseDatabase(current_app.config['db']['postgres']) as cursor:
        cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
        schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
        result = []
        for con in cursor.fetchall():
            result.append(dict(zip(schema, con)))
        return render_template('detail.html', result = result)

@main_blueprint.route('/new_vacancy', methods=['GET', 'POST'])
def new_vacancy():
    print (session)
    if session:
        if session['role'] == 'admin':
            if 'add_button' in request.form:
                # try:
                company = session['user']
                description = 'Краткое описание отсутствует'
                name = request.form['name']
                full_description = request.form['full_description']
                salary = request.form['salary']
                email = request.form['email']
                address = request.form['address']
                print (company, description, name, full_description, salary, email, address)

                with UseDatabase(current_app.config['db']['postgres']) as cursor:
                    cursor.execute("""INSERT INTO vacancy(company, description, name, full_description, salary, email, address)
                    VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s')""" % (company, description, name, full_description, salary, email, address) )
                
            return render_template('vacancy.html')
        else:
            return "Нет доступа"
    else:
        return "Нет доступа"

# @main_blueprint.route('/posts/<int:id>')
# def button(id):
#     print (session)
#     with UseDatabase(current_app.config['db']['postgres']) as cursor:
#         cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
#         schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
#         result = []
#         for con in cursor.fetchall():
#             result.append(dict(zip(schema, con)))
#         return render_template('test.html', result = result)
