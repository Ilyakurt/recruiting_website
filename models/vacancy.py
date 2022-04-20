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