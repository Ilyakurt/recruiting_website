from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class EmployerModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    def employer_company_profile(self, company):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT company, description
                FROM company_profile
                WHERE company = '%s'
                """ % (company))
            schema = ['company', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result