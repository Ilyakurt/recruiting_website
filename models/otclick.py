from flask import render_template, request, session, redirect, Blueprint, current_app, url_for
from DBCM import UseDatabase


class OtclickModel:
    def __init__(self, role):
        self.permission = role
        print ('role is', role)

    def select_otclick(self, user_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT
					u.id_vac,
					count(u.id_user)
                FROM user_vacancy u
                JOIN vacancy v
                ON u.id_vac = v.id
				WHERE v.id_user = %s
				GROUP BY
					u.id_vac
            """ % (user_id))
            schema = ['id_vac', 'count']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def vacancy_resume(self, id_vac):
        with UseDatabase(current_app.config['db'][self.permission]) as cursor:
            cursor.execute("""
                SELECT 
                    u.resume_id,
                    u.id_user, 
                    p.name, 
                    p.last_name, 
                    p.region,
                    r.about
                FROM user_vacancy u
                JOIN profile p 
                    ON u.id_user = p.user_id
                JOIN resume r
                    ON p.user_id = r.user_id
                        AND u.resume_id = r.resume_id
                WHERE 1 = 1
                    AND id_vac = %s
            """ % (id_vac))
            schema = ['resume_id', 'id_user', 'name', 'last_name', 'region', 'about']
            result = []
            for con in cursor.fetchall():
                result.append(dict(zip(schema, con)))
        return result

    def check_user(self, id_user, vac_id):
        with UseDatabase(current_app.config['db']['postgres']) as cursor:
            cursor.execute("""
                SELECT count(*) 
                FROM vacancy
                WHERE id_user = %s
                    AND id = %s
                """ % (id_user, vac_id))
            res = str(cursor.fetchone())
        result = res[1:-2]
        return result      