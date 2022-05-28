from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class VacancyModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    def add_vacancy(self, user_id):
        result = []
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""SELECT login, password, role, user_id, comp_name
                              FROM users
                              WHERE user_id = %s
                              """, (user_id))
            schema = ['login', 'password', 'role', 'user_id', 'comp_name']
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def select_response(self, user_id):
        print (user_id)
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT u.id_vac, v.name, u.id_user, u.status, p.name, p.last_name
                FROM user_vacancy u
                JOIN vacancy v
                ON u.id_vac = v.id
				JOIN profile p
				ON u.id_user = p.user_id
                WHERE v.id_user = %s
            """ % (user_id))
            schema = ['id_vac', 'name', 'id_user', 'status']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def employer_company_profile(self, company):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT company, description
                FROM company
                WHERE company = '%s'
                """ % (company))
            schema = ['company', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result
