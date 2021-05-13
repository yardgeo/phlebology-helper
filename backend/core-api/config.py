import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://phlb_viewer:phlb_viewer@130.193.52.22:5432/phlb_viewer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    RUN_PORT = os.environ.get('RUN_PORT') or 8080
    NUM_ROUND = os.environ.get('NUM_ROUND') or 1

    # security settings
    JWT_ISSUER = os.environ.get('JWT_ISSUER') or 'com.yardgeo.phlebology-helper'
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'phlebology-helper-secret'
    JWT_LIFETIME_SECONDS = os.environ.get('JWT_LIFETIME_SECONDS') or 7200
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'HS256'
    NUMBER_HASH_ITERATIONS = os.environ.get('NUMBER_HASH_ITERATIONS') or 100000
    HASH_ALGORITHM = os.environ.get('HASH_ALGORITHM') or 'sha256'

    # email settings
    TEMPLATE_PATH = os.environ.get('TEMPLATE_PATH') or 'templates'
    RECOVERY_CODE_LEFT_RANGE = os.environ.get('RECOVERY_CODE_LEFT_RANGE') or 100000
    RECOVERY_CODE_RIGHT_RANGE = os.environ.get('RECOVERY_CODE_RIGHT_RANGE') or 999999
    SMTP_ADDRESS = os.environ.get('SMTP_ADDRESS') or 'yardgeomailbot@gmail.com'
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or 'admin_mail'
    SMTP_HOST = os.environ.get('SMTP_HOST') or 'smtp.gmail.com'
    SMTP_PORT = os.environ.get('SMTP_PORT') or 587

    # orthanc
    ORTHANC_USER = os.environ.get('ORTHANC_USER') or 'orthancUser'
    ORTHANC_PASSWORD = os.environ.get('ORTHANC_PASSWORD') or 'orthancSecretPassword'
    ORTHANC_URL = os.environ.get('ORTHANC_URL') or 'http://84.252.141.49:8042/'

    # auto segmenatation
    PRETRAINED_IMG_SIZE = os.environ.get('PRETRAINED_IMG_SIZE') or 128
    PRETRAINED_MODEL_PATH = os.environ.get('PRETRAINED_MODEL_PATH') or 'data/model6'
