import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BREEZY_MAIL_SUBJECT_PREFIX = '[Breezy]'
    BREEZY_MAIL_SENDER = 'Breezy Admin <Breezy@example.com>'
    BREEZY_ADMIN = os.environ.get('Breezy_ADMIN')
    # UPLOAD_FOLDER = '/Users/allahesharghi/Desktop/Omid/pythonprojects/sound/sound/uploads'
    # ALLOWED_EXTENSIONS = set(['m4a'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    WTF_CSRF_ENABLED = False
    # UPLOAD_FOLDER = '/Users/allahesharghi/Desktop/Omid/pythonprojects/sound/sound/uploads'
    # ALLOWED_EXTENSIONS = 'm4a'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False
    # UPLOAD_FOLDER = '/Users/allahesharghi/Desktop/Omid/pythonprojects/sound/sound/uploads'
    # ALLOWED_EXTENSIONS = set(['m4a'])

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    WTF_CSRF_ENABLED = False
    # UPLOAD_FOLDER = '/Users/allahesharghi/Desktop/Omid/pythonprojects/sound/sound/uploads'
    # ALLOWED_EXTENSIONS = set(['m4a'])

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }