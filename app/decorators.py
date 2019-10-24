from flask import  session,redirect,render_template,url_for
from functools import wraps
from app import routes


#只有管理员登陆后才返回后台界面
def login_required(func):
    @wraps(func)
    def wrapper1(*args,**kwargs):
        #获取登陆时添加到cookie中的数据，如果能获得，说明登陆了，才返回管理员后台界面
        admin_login=session.get('user_telephone')
        if admin_login and admin_login=='13060220694':
                return func(*args,**kwargs)
        else:
            return redirect(url_for('/'))
    return wrapper1





