# -*- coding:utf-8 -*-
from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message=u"please fill in this field."), Length(1, 64), Email(message=u"Please fill in a valid email.")])
    password = PasswordField(u'password', validators=[DataRequired(message=u"please fill in this field."), Length(6, 32)])
    remember_me = BooleanField(u"keep logged in", default=True)
    submit = SubmitField(u'login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message=u"please fill in this field."), Length(1, 64), Email(message=u"please input a valid Email ?")])
    name = StringField(u'username', validators=[DataRequired(message=u"please fill in this field."), Length(1, 64)])
    password = PasswordField(u'password',
                             validators=[DataRequired(message=u"please fill in this field."), EqualTo('password2', message=u'passwords must match'),
                                         Length(6, 32)])
    password2 = PasswordField(u'please confirm password', validators=[DataRequired(message=u"please fill in this field.")])
    submit = SubmitField(u'register')

    def validate_email(self, filed):
        if User.query.filter(db.func.lower(User.email) == db.func.lower(filed.data)).first():
            raise ValidationError(u'email exists')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'original password', validators=[DataRequired(message=u"please fill in this field.")])
    new_password = PasswordField(u'new passwprd', validators=[DataRequired(message=u"please fill in this field."),
                                                     EqualTo('confirm_password', message=u'passwords don\'t match'),
                                                     Length(6, 32)])
    confirm_password = PasswordField(u'confirm password', validators=[DataRequired(message=u"please fill in this field.")])
    submit = SubmitField(u"save password")

    def validate_old_password(self, filed):
        from flask_login import current_user
        if not current_user.verify_password(filed.data):
            raise ValidationError(u'password incorrect')
