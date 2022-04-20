from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class UsersModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    # добавление пользователя (если успешно, то возвращает id нового пользователя, иначе - None)
    def insert_users(self, login, password, role):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                INSERT INTO users (login, password, role)
	            SELECT %s, %s, %s
            	FROM users
                WHERE NOT EXISTS (
                    SELECT login FROM users WHERE login = %s
                ) LIMIT 1
                RETURNING user_id""", (login, password, role, login))
            result = str(cursor.fetchone())
            print (result)
        return result