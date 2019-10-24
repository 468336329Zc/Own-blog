from email.mime.multipart import MIMEMultipart
import random
import smtplib
from email.mime.text import MIMEText



def randomnumber():
    checkcode = ""
    for i in range(6):
        current = random.randrange(0, 9, 2)
        if current != i:
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)
    print('随机验证码是:'+checkcode)
    return checkcode





def sendqqmail(_to,msginfo, html=True):
    _user = "468336329@qq.com"
    _pwd = "gukdprosazyjbhcb"  #qq邮箱smtp码
     #收件人

    msg = MIMEMultipart('alternative')
    msg["Subject"] = "[小张博客]注册验证通知"  #邮件主题
    msg["From"] = _user
    msg["To"] = _to
    if html:
        text = MIMEText(msginfo, 'html', 'utf-8')
        msg.attach(text)
    else:
        text = MIMEText(msginfo.encode("utf-8"))
        msg.attach(text)
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print(" Send Success!")
    except smtplib.SMTPException as e:
        print("Send Falied,%s" % e)


