from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class Quiz:
    def __init__(self, role):
        self.permission = role

    def get_subject(self):
            with UseDatabase(current_app.config['db']['client']) as cursor:
                cursor.execute("""
                    SELECT qid, subject, status 
                    FROM quiz
                    WHERE status = 2
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
                WHERE 1 = 1
                    AND qid = %s
                """ % (qid))
            schema = ['qid', 'question', 'check', 'option1', 'option2', 'option3', 'option4', 'qq_id']
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

    def select_quiz(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                    SELECT subject, status, qid, description
                    FROM quiz 
                    WHERE user_id = %s
                    ORDER BY qid
                """ % (user_id))
            schema = ['subject', 'status', 'qid', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result

    def select_quiz_count(self, qid):
        with UseDatabase(current_app.config['db']['client']) as cursor:
            cursor.execute("""
                SELECT count(*)
                FROM quiz_question
                WHERE qid = %s
                """ % (qid))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            return result

    def delete_quiz_question(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                DELETE
                FROM quiz_question
                WHERE qid = %s
                """ % (qid))
            result = 'Success'
        return result


    # def select_quiz_vacancy(self, user_id, qid):
    #     with UseDatabase(current_app.config['db']['client']) as cursor:
    #         cursor.execute("""
    #             SELECT count(*)
    #             FROM quiz_question
    #             WHERE qid = %s
    #             """ % (qid))
    #         schema = ['subject', 'status', 'qid', 'description']
    #         result = []
    #         for con in cursor.fetchall():
    #             result.append(dict(zip(schema, con)))
    #         return result

    def create_quiz(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                INSERT INTO quiz (subject, status, description, user_id)
                VALUES ('Тест', 0, 'Описание', %s)
                RETURNING qid
            """ % (user_id))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def edit_quiz(self, subject, description, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE quiz 
                    SET subject = '%s', 
                    description = '%s'
                WHERE qid = %s
                RETURNING qid
            """ % (subject, description, qid))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def select_quiz_edit(self, user_id, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                    SELECT subject, status, qid, description
                    FROM quiz 
                    WHERE user_id = %s
                    AND qid = %s
                """ % (user_id, qid))
            schema = ['subject', 'status', 'qid', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result

    def quiz_description(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                    SELECT subject, qid, description
                    FROM quiz 
                    WHERE 1 = 1 
                    AND qid = %s
                """ % (qid))
            schema = ['subject','qid', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result

    def quiz_attach(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                    SELECT subject, status, qid, description
                    FROM quiz 
                    WHERE user_id = %s
                    AND status = 1
                """ % (user_id))
            schema = ['subject', 'status', 'qid', 'description']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result


    def delete_quiz(self, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                DELETE 
                FROM quiz 
                WHERE 
                    qid = %s
            """ % (qid))
            result = 'Success'
        return result

        
    def update_quiz_question(self, question_str, option1, option2, option3, option4, check, qid):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                INSERT INTO quiz_question (question, option1, option2, option3, option4, answer, qid)
                VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s)
                RETURNING qid
            """ % (question_str, option1, option2, option3, option4, check, qid))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def count_right_answer(self, user_id, qid):
        with UseDatabase(current_app.config['db']['client']) as cursor:
            cursor.execute("""
                SELECT count(*)
                FROM public.quiz_user_answers a
                JOIN public.quiz_question q
                ON a.qid = q.qid
                    AND a.answer = q.answer
                WHERE 1 = 1
                    AND user_id = %s
                    AND q.qid = %s
                """ % (user_id, qid))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            return result

    def update_status(self, qid, status):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                UPDATE quiz 
                    SET status = %s
                WHERE 
                    qid = %s
                RETURNING qid
            """ % (status, qid))
            res = str(cursor.fetchone())
            result = res[1:len(res) - 2]
            print ("res", result)
        return result

    def quiz_check(self):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                    SELECT 
                        q.subject,
                        q.qid,
                        q.description,
                        q.status,
                        e.company,
                        e.email
                    FROM public.quiz q
                    JOIN public.employers e
                        ON q.user_id = e.user_id
                    WHERE 1 = 1
                        AND q.status IN (4, 5)
                """)
            schema = ['subject', 'qid', 'description', 'status', 'company', 'email']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
            return result