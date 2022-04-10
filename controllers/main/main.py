from asyncio import constants
from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/')
def main():
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
    with UseDatabase(current_app.config['db']['postgres']) as cursor:
        cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
        schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
        result = []
        for con in cursor.fetchall():
            result.append(dict(zip(schema, con)))
        return render_template('test.html', result = result)

@main_blueprint.route('/new_vacancy', methods=['GET', 'POST'])
def new_vacancy():
    if 'add_button' in request.form:
        # try:
        company = 'tele2'
        description = 'kek'
        name = request.form['name']
        full_description = request.form['full_description']
        salary = request.form['salary']
        email = request.form['email']
        address = request.form['address']
        print (company, description, name, full_description, salary, email, address)
        # except:
        #     company = 'tele2'
        #     description = 'kek'
        #     name = 'kek'
        #     full_description ='kek'
        #     salary = 100
        #     email = 'kek'
        #     address = 'kek'
        #     print (id, company, description, name, full_description, salary, email, address)

        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""INSERT INTO vacancy(company, description, name, full_description, salary, email, address)
            VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s')""" % (company, description, name, full_description, salary, email, address) )

    return render_template('vacancy.html')

# def add_vacancy(data):

    
    
    # cursor.execute("""INSERT INTO vacancy(id, company, description, name, full_description, salary, email, address)
    #     VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (id, company, description, cursor, name, full_description, salary, email, address))