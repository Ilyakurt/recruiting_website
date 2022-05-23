from app import configureApp
from flask import Flask, render_template

app = Flask(__name__)

from DBCM import error_blueprint
app.register_blueprint(error_blueprint, url_prefix='/error')

from controllers.auth.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from controllers.quiz.quiz import quiz_blueprint
app.register_blueprint(quiz_blueprint, url_prefix='/quiz')

from controllers.auth.auth import logout_blueprint
app.register_blueprint(logout_blueprint, url_prefix='/logout')

from controllers.main.main import main_blueprint
app.register_blueprint(main_blueprint, url_prefix='/')

from controllers.profile.profile import profile_blueprint
app.register_blueprint(profile_blueprint, url_prefix='/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_url.html'), 404

if __name__ == '__main__':
    app = configureApp(app)
    app.run (
        debug=app.config['server']['debug'], 
        host=app.config['server']['host'], 
        port=app.config['server']['port']
    )
