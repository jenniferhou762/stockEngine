# -*- coding: utf-8 -*-

from app import app, db
from app.models import User, Role, Investment

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

admin = User(name=u'root', email='root@gmail.com', password='password', major='administrator',
             headline=u"administrator", about_me=u"administrator")
user1 = User(name=u'Jing', email='jing@gmail.com', password='123456', major='Software Engineering', headline=u"student")
user2 = User(name=u'test', email='test@gmail.com', password='123456')
user3 = User(name=u'alex', email='alex@gmail.com', password='123456')
user4 = User(name=u'ben', email='ben@gmail.com', password='123456')


investments = [Investment(user1, 6000, "Ethical Investing,Growth Investing"), Investment(user1, 7000, "Ethical Investing,Index Investing"),
 Investment(user2, 8000, "Index Investing,Quality Investing"), Investment(user3, 9000, "Index Investing,Value Investing")]

db.session.add_all([admin, user1, user2, user3, user4] + investments)
db.session.commit()

app_ctx.pop()
