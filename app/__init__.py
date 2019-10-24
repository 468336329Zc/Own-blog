
from flask import Flask, config

#导入配置文件
from config import Config
#导入数据
from flask_sqlalchemy import SQLAlchemy

#初始化一个Flask对象
#Flask()
#需要传递一个参数   __name__

application = Flask(__name__)
# 添加配置信息
application.config.from_object(Config)
# 初始化app应用实例
# 建立数据库关系
db = SQLAlchemy(application)
#添加路由
from app import routes,models

