from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class PostsModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    def select_post(self, id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
            schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def search_vacancy(self, name):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT company, description, salary, name, id 
                FROM vacancy
                WHERE 1 = 1 
                    AND ( 
                        LOWER(name) LIKE LOWER('%%%s%%')
                        OR LOWER(company) LIKE LOWER('%%%s%%')
                        OR LOWER(description) LIKE LOWER('%%%s%%')
                    )
            """ % (name, name, name))
            schema = ['company', 'description', 'salary', 'name', 'id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def otclick(self, id, user, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""INSERT INTO user_vacancy(id_vac, id_user, resume_id) VALUES (%s, %s, %s) RETURNING status""" % (id, user, resume_id))
            res = str(cursor.fetchone())
        result = res[1:len(res) - 2]
        return result