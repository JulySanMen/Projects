import os

class Conf:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:G170122fg#@localhost/Cuest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
