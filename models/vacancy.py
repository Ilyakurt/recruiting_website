from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class VacancyModel:
    def __init__(self, role):
        self.permission = role

    def select_response(self):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT * FROM user_vacancy
            """)
            schema = ['id_vac', 'id_user', 'status']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            result = str(cursor.fetchall())
        return result

    def user_vacancy(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT company, description, salary, name, id, status
                FROM vacancy
                WHERE id_user = %s
                ORDER BY id
            """  % (user_id))
            schema = ['company', 'description', 'salary', 'name', 'id', 'status']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def user_vacancy_status_salary_update(self, vac_id, status, salary):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                UPDATE vacancy
                SET status = %s, salary = %s
                WHERE id = %s
                RETURNING id
            """  % (status, salary, vac_id))
            result = str(cursor.fetchone())
        return result