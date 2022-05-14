from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class Quiz:
    # def __init__(self, role):
    #     self.permission = role

    # добавление пользователя (если успешно, то возвращает id нового пользователя, иначе - None)
    def get_subject(self):
            with UseDatabase(current_app.config['db']['client']) as cursor:
                cursor.execute("""
                    SELECT qid, subject, status 
                    FROM quiz
                    """)
                schema = ['qid', 'subject', 'status']
                result = []
                for con in cursor.fetchall():
                    result.append(dict(zip(schema, con)))
                return result

    # def create_subject(self):
    #     with UseDatabase(current_app.config['db']['postgres']) as cursor:
    #         cursor.execute("""
    #             SELECT qid, subject, question, answer, status 
    #             FROM quiz
    #             """)
    #         result = []
    #         for con in cursor.fetchall():
    #             result.append(dict(zip(schema, con)))
    #         return result

    def select_description(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT qid, subject, description 
                FROM quiz
                WHERE qid = %s 
                """ % (qid))
            schema = ['qid', 'subject', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result
    
    def quiz_question(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT qid, question, answer, option1, option2, option3, option4, qq_id
                FROM quiz_question
                WHERE qid = %s
                """ % (qid))
            schema = ['qid', 'question', 'answer', 'option1', 'option2', 'option3', 'option4', 'qq_id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result

    def quiz_id(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT qq_id
                FROM quiz_question
                WHERE qid = %s
                """ % (qid))
            schema = ['qq_id']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result

    def user_result_insert(self, qid, qq_id, answer, type_answer, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                INSERT INTO quiz_user_answers (qid, qq_id, answer, type_answer, user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id
                """ % (qid, qq_id, answer, type_answer, user_id))
            result = str(cursor.fetchone())
            print (result)
        return result