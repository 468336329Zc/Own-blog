from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Email,URL,Length,Optional
from wtforms import HiddenField
#普通用户评论表单
class CommentForm(FlaskForm):
    author=StringField('name',validators=[DataRequired(),Length(1,30)])
    email=StringField('email',validators=[DataRequired(),Email,Length(1,254)])
    site=StringField('site',validators=[Optional(),URL(),Length(0,255)])
    body=StringField('Comment',validators=[Optional(),URL(),Length(0,255)])
    submit=SubmitField()

#管理员评论表单
class AdminCommentForm(CommentForm):
    author=HiddenField()
    email =HiddenField()
    site=HiddenField()


class LoginForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    verify_code = StringField('验证码', validators=[DataRequired()])
    remember_me = BooleanField('记住自己的用户')
    submit = SubmitField('登录')





