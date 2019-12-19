#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.views import csrf
from flask import Flask, render_template, request, redirect, session, Response, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column

from models import config
import os
from datetime import timedelta,datetime
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') # Change default encoding to utf8
app = main = Flask(__name__, template_folder='../', static_folder='../include')
app.config.from_object(config)
db = SQLAlchemy(app)
app.config["JSON_AS_ASCII"] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SECRET_KEY'] = os.urandom(24)


class UserInfo(db.Model):
    table_name = 'userinfo'
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户')
    username = db.Column(db.String(100), nullable=False, server_default='', comment='用户账号')
    password = db.Column(db.String(100), nullable=False, server_default='', comment='用户密码')
    jianjie = db.Column(db.String(1000), nullable=False, server_default='', comment='用户简介')
    email = db.Column(db.String(100), nullable=False, server_default='', comment='邮箱')
    registrationTime = db.Column(db.DateTime, nullable=False, server_default=func.now(),  comment='注册时间')


class article(db.Model):
    table_name = 'article'
    ArticleId = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='文章编号')
    title = db.Column(db.String(100), nullable=False, server_default='', comment='文章标题')
    content = db.Column(db.String(10000), nullable=False, server_default='',  comment='文章内容')
    creator = db.Column(db.String(100), nullable=False, server_default='', comment='文章作者')
    createTime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='发布时间')

class Comment(db.Model):
    table_name = 'comment'
    commentId = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='评论编号')
    ArticleId = db.Column(db.String(10), nullable=False, server_default='', comment='文章编号')
    content = db.Column(db.String(100), nullable=False, server_default='', comment='评论内容')
    creator = db.Column(db.String(100), nullable=False, server_default='', comment='评论作者')
    createTime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='评论时间')
    status = db.Column(db.String(10),nullable=False,server_default='N',comment='评论状态')

class Image(db.Model):
    table_name = 'image'
    ImageId = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='图片编号')
    image = db.Column(db.String(100), nullable=False, server_default='', comment='文章图片')

db.drop_all()
db.create_all()

#上传图片方法
@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    f = request.files['image']
    date = str(datetime.now())#以当前时间命名
    f.filename = date.replace(" ", '')#去掉路径特殊字符
    f.filename = f.filename.replace(".", '')
    f.filename = f.filename.replace(":", '') + ".jpg"
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path = os.path.join(basepath, '../include/images/', secure_filename(f.filename))
    f.save(upload_path)#保存图片
    data = Image(image="../include/images/" + f.filename)#获取数据对象
    db.session.add(data)
    db.session.commit()
    return redirect('/edit/')

@app.route('/uploader/', methods=['GET', 'POST'])
def upload_file():#富文本编辑器的图片上传
    if request.method == 'POST':
        img = request.files.get('file')
        print(img)
        basepath = os.path.dirname(os.path.dirname(__file__))  # 当前文件所在路径
        upload_path = os.path.join(basepath,'include','images', secure_filename(img.filename))
        imgsrc = '../include/images/'+secure_filename(img.filename)
        img.save(upload_path)
        mes = {}
        mes['location'] = imgsrc       # 将图片的地址封装在字典里,键为path,这样图片就能在富文本中显示了
        return jsonify(mes)



#首页方法
@app.route('/', methods=['POST', 'GET'])
def index():
    sql = 'select * from article,image where Articleid = imageid'#
    data = db.session.execute(sql)#执行sql语句
    image = Image.query.filter().all()[1:3]#首页轮播图
    left = UserInfo.query.filter().all()#推荐作者信息
    if session.get('username'):
        user = UserInfo.query.filter(UserInfo.username==session.get('username')).first()#查用户信息
        return render_template('views/index.html', data=data, image=image, left=left,user=user)
    else:
        return render_template('views/index.html', data=data, image=image, left=left)

#编辑文本
@app.route('/edit/', methods=['POST', 'GET'])
def editarticle():
    if session.get('username'):
        user = UserInfo.query.filter(UserInfo.username == session.get('username')).first()
        data = []
        return render_template('views/editarticle.html',data=data,user=user)
    else:
        return redirect('/')

#查看注册页面
@app.route('/registerPage/', methods=['POST', 'GET'])
def registerPage():
    return render_template('views/register.html')

#注册方法
@app.route('/register/', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    jianjie = request.form.get('jianjie')
    user_info = UserInfo(username=username, password=password, email=email,jianjie=jianjie)
    db.session.add(user_info)
    db.session.commit()
    alert = "<script>alert('注册成功！')<script>;"
    load = "\"window.location.href = '/'\""
    return render_template('views/register.html', alert=alert, load=load)

#登录方法
@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = UserInfo.query.filter(UserInfo.username == username, UserInfo.password == password).first()
    if user:
        session['username'] = username
        return redirect('/')
    else:
        return redirect('registerPage')


#查看文章内容方法
@app.route('/article_Content/', methods=['GET', 'POST'])
def articleContent():
    id = request.args.get('id')
    data = article.query.filter(article.ArticleId == id).first()
    #查看文章评论
    if session.get('username'):
        user = UserInfo.query.filter(UserInfo.username == session.get('username')).first()
        comment = Comment.query.filter(Comment.ArticleId == id).all()
        return render_template('views/article_Content.html', data=data, comment=comment,id=id,user=user,tag=False)
    else:
        comment1 = "<h4 style='text-align:center;margin-top:85px;'>您尚未登录无法查看评论内容，<a href='/registerPage'>登录或注册</a><h4>"
        return render_template('views/article_Content.html', data=data,comment1=comment1,tag=True)

#提交文章内容方法
@app.route('/insertContent/', methods=['GET', 'POST'])
def insertContent():
    title = request.form.get('title')
    content = request.form.get('content')
    username = session.get('username')
    data = article(title=title,content=content,creator=username)
    db.session.add(data)
    db.session.commit()
    return redirect('/')


#发表评论方法
@app.route('/insertComment/', methods=['GET', 'POST'])
def insertComment():
    id = request.form.get('id')
    content = request.form.get('content')
    username = session.get('username')
    data = Comment(content=content, creator=username, ArticleId=id)
    db.session.add(data)
    db.session.commit()
    return redirect('/article_Content/?id='+id)

#查看文章方法
@app.route('/articleList/',methods=['GET','POST'])
def articleList():
    data=article.query.filter().all()
    left = UserInfo.query.filter().all()
    if session.get('username'):
        user = UserInfo.query.filter(UserInfo.username==session.get('username')).first()
        return render_template('views/articlelist.html', data=data,left=left,user=user)
    else:
        return render_template('views/articlelist.html', data=data,left=left )
    # return render_template('views/articlelist.html', data=data)

#查看文章专题
@app.route('/part/',methods=['GET','POST'])
def part():
    return render_template('views/part.html')

#后台文章删除内容
@app.route('/delete/', methods=['GET','POST'])
def delete():
    id = request.args.get('id')
    article.query.filter(article.ArticleId==id).delete()
    Comment.query.filter(Comment.commentId == id).delete()
    db.session.commit()
    return redirect('/articleList/')


#删除评论
@app.route('/delete_comment/', methods=['GET','POST'])
def delete_comment():
    id = request.args.get('id')
    page = request.args.get('page')
    Comment.query.filter(Comment.commentId == id).delete()
    db.session.commit()
    return redirect('/article_Content/?id='+page)

#个人信息
@app.route('/personal/', methods=['GET','POST'])
def persion():
    username = session.get('username')
    data = article.query.filter(article.creator==username).all()
    user = UserInfo.query.filter(UserInfo.username == session.get('username')).first()
    return render_template('views/personal.html',data=data,user=user)

#后台修改内容
@app.route('/adminEdit/', methods=['GET','POST'])
def admin():
    id = request.args.get('id')
    data = article.query.filter(article.ArticleId == id).first()
    if session.get('username'):
        user = UserInfo.query.filter(UserInfo.username==session.get('username')).first()
        return render_template('views/admin/index.html',data=data,id=id,user=user)
    else:
        return render_template('views/admin/index.html', data=data,)

#更新内容
@app.route('/updateContent/',methods=['GET','POST'])
def updateContent():
    id = request.form.get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    article.query.filter(article.ArticleId == id).update({"title":title,"content":content})
    db.session.commit()
    return redirect('/articleList/')

#注销
@app.route('/zhuxiao/',methods=['GET','POST'])
def zhuxiao():
    session.clear()#删除所有session
    return redirect('/')




if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True)