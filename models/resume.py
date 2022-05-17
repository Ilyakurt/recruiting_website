from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class ResumeModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    def select_user(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT name, last_name, email, phone_number, region, user_id
                FROM profile 
                WHERE user_id = %s
            """ % (user_id))
            schema = ['name', 'last_name', 'email', 'phone_number', 'region', 'user_id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def select_resume(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT position_work, specialization, salary, user_id, about, resume_id, status
                FROM resume 
                WHERE user_id = %s
                ORDER BY resume_id
            """ % (user_id))
            schema = ['position_work', 'specialization', 'salary', 'user_id', 'about', 'resume_id', 'status']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def resume_edit(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT position_work, specialization, salary, user_id, about, resume_id
                FROM resume 
                WHERE user_id = %s
                    AND resume_id = %s
            """ % (user_id, resume_id))
            schema = ['position_work', 'specialization', 'salary', 'user_id', 'about', 'resume_id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def select_resume_experience(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id
                FROM resume_experience 
                WHERE user_id = %s
                    AND resume_id = %s
            """ % (user_id, resume_id))
            schema = ['company', 'start_dttm', 'end_dttm', 'region', 'position_work', 'charge', 'user_id', 'resume_id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result
    
    def create_resume(self, user_id):
        specialization = 'NULL'
        salary = 'NULL'
        about = 'NULL'
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                INSERT INTO resume (position_work, specialization, salary, user_id, about, status)
                VALUES ('Начинающий специалист', %s, %s, %s, %s, 0)
                RETURNING resume_id
            """ % (specialization, salary, user_id, about))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def create_resume_experience(self, user_id, resume_id):
        company = 'NULL'
        start_dttm = 'NULL'
        end_dttm = 'NULL'
        region = 'NULL'
        position_work = 'NULL'
        charge = 'NULL'
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                INSERT INTO resume_experience (company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING resume_id
            """ % (company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def delete_resume(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                DELETE FROM resume
                WHERE user_id = %s
                    AND resume_id = %s
            """ % (user_id, resume_id))
            result =['Успешно']
            print ("res", result)
        return result
    
    def delete_resume_experience(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                DELETE FROM resume_experience
                WHERE user_id = %s
                    AND resume_id = %s
            """ % (user_id, resume_id))
            result =['Успешно']
            print ("res", result)
        return result

    def active_resume(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE resume
                SET status = 1
                WHERE user_id = %s
                    AND resume_id = %s
                RETURNING resume_id
            """ % (user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def deactivation_resume(self, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE resume
                SET status = 0
                WHERE user_id = %s
                    AND resume_id = %s
                RETURNING resume_id
            """ % (user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def update_position(self, user_id, position_work, specialization, salary, resume_id):
        if len(salary) < 1:
            salary = 'NULL'
        print (salary)
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE resume
                SET 
                    position_work = '%s',
                    specialization= '%s', 
                    salary= %s
                WHERE user_id = %s
                    AND resume_id = %s
                RETURNING resume_id
            """ % (position_work, specialization, salary, user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def update_experience(self, company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE resume_experience
                SET 
                    company = '%s',
                    start_dttm= '%s', 
                    end_dttm = '%s',
                    region = '%s',
                    position_work = '%s',
                    charge = '%s'
                WHERE user_id = %s
                    AND resume_id = %s
                RETURNING resume_id
            """ % (company, start_dttm, end_dttm, region, position_work, charge, user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def update_about(self, user_id, about, resume_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE resume
                SET 
                    about = '%s'
                WHERE user_id = %s
                    AND resume_id = %s
                RETURNING resume_id
            """ % (about, user_id, resume_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def select_response(self, user_id):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT u.id_vac, v.name, u.id_user, u.status, v.company, salary
                FROM user_vacancy u
                JOIN vacancy v
                ON u.id_vac = v.id
                WHERE u.id_user = %s
            """ % (user_id))
            schema = ['id_vac', 'name', 'id_user', 'status', 'company', 'salary']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result