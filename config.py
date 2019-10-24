import os
from flask import jsonify
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG=True
    #数据库格式   dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask-blog'
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    #session加密的密钥,s=随机的24位数
    SECRET_KEY=os.urandom(24)

