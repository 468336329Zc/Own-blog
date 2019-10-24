from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from app import application,db





"""
想处理哪个模型，就导入哪个模型
"""


"""
flaskweb应用实例app与数据库绑定，使用Migrate库 方便操作web应用于数据库

数据库模型迁移：   模型--->迁移文件-->数据库中表创建

"""
manager=Manager(application)

#绑定app和数据库，以便进行操作web应用app与数据库
migrate = Migrate(application,db)
#把MigrateCommand命添加到manager中
manager.add_command('db',MigrateCommand)

if __name__=="__main__":
    manager.run()