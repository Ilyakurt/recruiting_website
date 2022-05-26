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
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
        return result

    def insert_employer_to_users(self, login, password, role):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                INSERT INTO users (login, password, role)
	            SELECT %s, %s, %s
            	FROM users
                WHERE NOT EXISTS (
                    SELECT login FROM users WHERE login = %s
                ) LIMIT 1
                RETURNING user_id""", (login, password, role, login))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
        return result

    def insert_company(self, company, status):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                INSERT INTO company (company, status)
	            SELECT %s, %s
                RETURNING company""", (company, status))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
        return result

    def insert_employer(self, name, last_name, company, phone, email, city, address, user_id, status):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                INSERT INTO employers (name, last_name, company, phone, email, city, address, user_id, status)
	            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s
                RETURNING user_id""", (name, last_name, company, phone, email, city, address, user_id, status))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
        return result

    def profile_create(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                INSERT INTO profile (user_id)
                VALUES (%s)
                RETURNING user_id
                """ % (user_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def profile(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT name, last_name, email, phone_number, region, status
                FROM profile
                WHERE user_id = %s
                """ % (user_id))
            schema = ['name', 'last_name', 'email', 'phone_number', 'region', 'status']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def profile_employer(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT name, last_name, company, email, phone, city, address
                FROM employers
                WHERE user_id = %s
                """ % (user_id))
            schema = ['name', 'last_name', 'company', 'email', 'phone_number', 'region', 'address']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def company_employer(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT company
                FROM employers
                WHERE user_id = %s
                """ % (user_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
        return result

    def phone_number_update(self, phone_number, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE profile
                    SET phone_number = %s
                    WHERE user_id = %s
                    RETURNING 1
                """ % (phone_number, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result

    def region_update(self, region, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE profile
                    SET region = '%s'
                    WHERE user_id = %s
                    RETURNING 1
                """ % (region, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result

    def email_update(self, email, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE profile
                    SET email = '%s'
                    WHERE user_id = %s
                    RETURNING 1
                """ % (email, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result

    def name_update(self, name, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE profile
                    SET name = '%s'
                    WHERE user_id = %s
                    RETURNING 1
                """ % (name, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result

    def last_name_update(self, name, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE profile
                    SET last_name = '%s'
                    WHERE user_id = %s
                    RETURNING 1
                """ % (name, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result

    def employer_company_profile(self, company):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            print (company)
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

    def employer_company_profile_edit(self, company, description):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                    UPDATE company
                    SET description = '%s'
                    WHERE company = '%s'
                    RETURNING 1
                """ % (description, company))
            result = str(cursor.fetchone())
            print (result)
        return result