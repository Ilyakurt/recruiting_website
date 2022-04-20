from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class PostsModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    # добавление пользователя (если успешно, то возвращает id нового пользователя, иначе - None)
    def select_post(self, id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""SELECT company, description, name, full_description, salary, email, address FROM vacancy WHERE id = %s""" % (id))
            schema = ['company', 'description', 'name', 'full_description', 'salary', 'email', 'address']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def otclick(self, id, user):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""INSERT INTO public.user_vacancy(id_vac, id_user) VALUES (%s, %s) RETURNING status""" % (id, user))
            res = str(cursor.fetchone())
        result = res[1:len(res) - 2]
        return result