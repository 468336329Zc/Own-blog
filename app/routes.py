# 从app文件中导入这个Flask对象app
import base64
import datetime

import numpy as np

from app.Util import Face_check, Pagination
import os
import re

from flask import redirect, render_template, request, url_for, session, Response, flash, make_response, json, jsonify
from app.emails import randomnumber, sendqqmail
from app import application, db
from app.decorators import login_required
from app.models import User, Blog,  Category
import json


@application.route("/")
def show_main_page():
    return render_template("auth/show_main_page.html")


@application.route('/face_login')
def face_login():
    return render_template('auth/face_login.html')


@application.route('/face_login/get_face', methods=['POST'])
def get_face():
    # 保存图片到本地
    # 这里给每张图片加一个时间 确保能正确比对应该比对的那张图片
    if request.method == 'POST':
        time = datetime.datetime.now().strftime('%Y%m%d&%H%M%S')
        strs = request.form.get('face_id')
        # 解码base64
        imgdata = base64.b64decode(strs)

        try:
            file = open('app/static/facedata/confirm/' + time + '.jpg', 'wb')
            file.write(imgdata)
            file.close()
        except:
            # json数据返回
            data = {"status": "-1"}
            return data
        # 查询所有的face_id
        try:
            bases64 = db.session.query(User.face_id).all()
        except:
            data = {'status': '-1'}
            return data
        for b64 in bases64:
            # 对每一个取出来的进行解码，写入register文件，之后在于confirm中的图片进行对比
            b64 = str(b64[0])
            img = base64.b64decode(b64)
            try:
                file2 = open('app/static/facedata/register/' + time + '.jpg', 'wb')
                file2.write(img)
                file2.close()
            except:
                # json数据返回
                data = {"status": "-1"}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/facedata/register/" + time + '.jpg')
                os.remove("app/static/facedata/confirm/" + time + '.jpg')
                return data
            time = datetime.datetime.now().strftime('%Y%m%d&%H%M%S')

            known_face_encoding = Face_check.register_encoding_face('app/static/facedata/register/' + time + '.jpg')

            try:
                match_results = Face_check.check_face(known_face_encoding,
                                                      "app/static/facedata/confirm/" + time + '.jpg')
            except:
                data = {"status": '-2'}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/facedata/register/" + time + '.jpg')
                os.remove("app/static/facedata/confirm/" + time + '.jpg')
                return data

            if match_results[0] == True:

                # 登录成功就加入session
                user = User.query.filter(User.face_id == b64).first()
                session['user_telephone'] = user.telephone
                print(user.telephone)
                data = {'status': '1'}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/facedata/register/" + time + '.jpg')
                os.remove("app/static/facedata/confirm/" + time + '.jpg')
                return data
            else:
                # 由于浏览器还是认为是text/html数据 因此使用mimetype说明是json数据
                data = jsonify({"status": "0", "face_distance": 'not one person'})
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/facedata/register/" + time + '.jpg')
                os.remove("app/static/facedata/confirm/" + time + '.jpg')
                return data
    else:
        return redirect('/404')


@application.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        # 获取登陆输入的数据
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        # 查找数据库中表数据进行比对
        user_have = User.query.filter(User.telephone == telephone)
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        # 如果有这个用户
        if user_have:
            # 如果密码不是空的
            if not password == '':
                # 如果是管理员
                if user.telephone == '13060220694':
                    # 若密码正确
                    if user:
                        # 保存cookie信息  31天内不用重复登陆
                        session['user_telephone'] = user.telephone
                        session.permanent = True
                        return redirect('/admin/')
                    else:
                        return render_template('auth/login.html')
                # 不是管理员
                else:
                    # 若密码正确 重定向返回上一个界面
                    if user:
                        session['user_telephone'] = user.telephone
                        session.permanent = True
                        return redirect('/articles/')
            # 密码是空的
            else:
                return render_template('auth/login.html')
        # 没有这个用户,重定向注册
        else:
            return redirect(url_for('register'))


@application.route("/admin/", methods=["GET", "POST"])
@login_required
def logined():
    if request.method == "GET":
        return render_template('admin/logined.html')
    else:
        return redirect('/')


@application.route('/send', methods=['GET'])
def send():
    if request.method == "GET":
        # 获取前台的数据
        data = request.args.get("data")
        # 反序列化前台传过来的json数据，使之变为字典
        json_data = json.loads(data)
        to = json_data['email']
        # 发送验证码
        global randomnber
        randomnber = randomnumber()
        sendqqmail(to, "<h3>验证你的电子邮件地址</h3>"
                       "<p>你的验证码是:{rdommnumber}</p><p>详情请看:</p><a>http:www.baidu.com</a>".format(
            rdommnumber=randomnber))
        return randomnber

    else:
        return redirect('/register')


@application.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")
    else:
        # 获取表单数据
        telephone = request.form.get("telephone")
        password1 = request.form.get("pwd")
        email = request.form.get("email")
        yanzhengma = request.form.get('yanzhengma')
        face_b64 = request.form.get('face_b64')

        # 手机号码验证，如果数据库中不存在  就允许注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            data = {"status": "0"}
            return data
        else:
            if yanzhengma != randomnber:
                data = {"status": "-1"}
                return data
            else:
                user = User(telephone=telephone, email=email, password=password1, face_id=face_b64)
                db.session.add(user)
                db.session.commit()
                data = {"status": "1"}
                return data


@application.route('/logout')
def logout():
    user_telephone = session.get('user_telephone')
    # 如果存在user_telephone
    if user_telephone:
        # 删除cookie信息
        session.pop('user_telephone')
        # 返回登陆界面
        login_url = url_for('login')
        return redirect(login_url)
    else:
        return render_template('auth/404.html')


@application.route('/articles/')
def articles():
    context = {
        # 只从数据库中查询最新发表的10篇显示出来
        'blogs': Blog.query.order_by(Blog.create_time.desc()).limit(10)

    }
    return render_template('auth/blog_center_articles.html', **context)


@application.route('/articles/detail/<blog_title>/', methods=['GET'])
def detail(blog_title):
    if request.method == 'GET':
        # 到数据库搜索与blog_title匹配的，返回
        blog = Blog.query.filter(Blog.title == blog_title).first()

        if blog:
            route_detail_contexts = {"blog": blog,

                                     }
            return render_template('auth/blog_center_articles_detail.html', **route_detail_contexts)
        else:
            return redirect(url_for('404.html'))


# 所有的文章
@application.route('/categories/')
def show_category():
    # 分页的对象
    li = []
    blognums = Blog.query.count()
    blogs = Blog.query.order_by(Blog.create_time.desc())
    for i in range(0, blognums):
        li.append(blogs[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=7)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()

    return render_template('auth/category.html', index_list=index_list, html=html)


# 标签
@application.route('/biaoqian/')
def biaoqian():
    return render_template('auth/biaoqian.html')


@application.route('/update/')
def update():
    return render_template('auth/update.html')


# 关于
@application.route('/about/', methods=['GET', "POST"])
def about():
    if request.method == "GET":
        return render_template('auth/about.html')
    else:
        return render_template('auth/404.html')



@application.route("/404", methods=['GET', "POST"])
def invalid():
    if request.method == "GET":
        return render_template("auth/404.html")
    else:
        return render_template('auth/404.html')


@application.route('/get_ip')
def get_ip():
    return jsonify({'ip': request.remote_addr})


###########前#####################前后台分界####################################后##########################
# 博客中心
@application.route('/blog-center')
def index():
    title = '博客管理中心'
    return render_template('auth/index.html', title=title)


@application.route('/markdown_editor1', methods=['GET', 'POST'])
@login_required
def markdown_editor1():
    if request.method == "GET":
        return render_template('admin/markdown_editor1.html')
    else:
        blog_title = request.form.get('title')
        blog_content = request.form.get('content')
        # 添加到数据库中
        blog = Blog(title=blog_title, content=blog_content)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('articles'))


# 再次编辑博文
@application.route('/editor-again/<blog_title>', methods=['GET', 'POST'])
@login_required
def editor_again(blog_title):
    if request.method == 'GET':
        blog = Blog.query.filter(Blog.title == blog_title).first()
        contexts = {"blog": blog}
        return render_template('admin/editor-again.html', **contexts)
    else:
        blog = Blog.query.filter(Blog.title == blog_title).first()
        blog_title = request.form.get('title')
        blog_content = request.form.get('content')
        # 修改数据
        blog.title = blog_title
        blog.content = blog_content
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('articles'))


@application.route('/admin/blog-ceter/publish_update')
@login_required
def publish_update():
    return render_template('admin/publish_update.html')


# 博客发布设置登陆限制
@application.route('/has_logined/', methods=["GET", "POST"])
@login_required
def login_require():
    if request.method == 'GET':
        return redirect(url_for('markdown_editor1'))
    else:
        return redirect(url_for('invalid'))


# 上下文钩子函数(全局变量)
@application.context_processor
def my_context_processer():
    # 如果登录了，就能获取sesson中的数据
    user_telephone = session.get('user_telephone')
    if user_telephone == '13060220694':
        # 与数据库中的数据进行比对
        user = User.query.filter(User.telephone == user_telephone).first()
        if user:
            # 返回用户
            return {'admin': user}
    return {}


@application.route('/delete/<blog_title>', methods=['GET'])
def delete(blog_title):
    if request.method == 'GET':
        blog = Blog.query.filter(Blog.title == blog_title).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect('/articles/')


@application.route('/admin/blog-center')
def blog_center():
    return render_template('admin/blog-center-base.html')


@application.route('/admin/blog-center/blogmanage')
@login_required
def blog_center_blogmanage():
    # 分页的对象
    li = []
    blognums = Blog.query.count()
    blogs = Blog.query.order_by(Blog.create_time.desc())
    for i in range(0, blognums):
        li.append(blogs[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=5)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('admin/blog-center-blogmanage.html', index_list=index_list, html=html)


@application.route('/admin/blog-center/comments-manage')
def comments_manage():
    return render_template('admin/comments-manage.html')


# 上下文
@application.context_processor
def admin_context():
    admin = User.query.filter(User.telephone == '13060220694').first()
    categories = Category.query.order_by(Category.name).all()
    blogs = Blog.query.order_by(Blog.create_time.desc())
    return {'admin2': admin.telephone == '13060220694',
            'categories': categories,
            'blogs': blogs}


