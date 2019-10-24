from flask import current_app

from app import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#数据库模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    telephone= db.Column(db.String(11), index=True, unique=True)
    email=db.Column(db.String(128),unique=True)
    password= db.Column(db.String(128))
    about=db.Column(db.TEXT)
    face_id=db.Column(db.Text)

    #生成验证码
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 这个函数需要两个参数，一个密匙，从配置文件获取，一个时间，这里1小时
        return s.dumps({'confirm': self.id})
        # 为ID生成一个加密签名，然后再对数据和签名进行序列化，生成令牌版字符串（就是一长串乱七八糟的东西）,然后返回


class Blog(db.Model):
    __tablename__='blog'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)

    #now函数是每一次创建一个博客就会有一个时间
    #now()是第一次执行这句语句的时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    #blog表与文章分类表Category关联
    category=db.relationship('Category',back_populates='blogs')


#文章分类
class Category(db.Model):
    __table__name='category'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    blogs=db.relationship('Blog',back_populates='category')

db.create_all()