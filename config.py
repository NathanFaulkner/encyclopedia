import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'squedvo@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'p6WdwKrpT9ufvRw'
    ADMINS = ['squedvo@gmail.com', 'nathanfaulkner@gmail.com']
    POSTS_PER_PAGE = 20
    SITE_NAME = 'Encyclopedia Omega'

    # MAIL_SERVER=smtp.googlemail.com
    # MAIL_PORT=587
    # MAIL_USE_TLS=1
    # MAIL_USERNAME=squedvo@gmail.com
    # MAIL_PASSWORD=p6WdwKrpT9ufvRw
