# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, URL
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField, FileAllowed
from app import avatars


class EditProfileForm(FlaskForm):
    name = StringField(u'username', validators=[DataRequired(message=u"please fill in this field!"), Length(1, 64, message=u"length must larger than one and smaller than 64")])
    major = StringField(u'major', validators=[Length(0, 128, message=u"length must large than 0 and smaller than 10")])
    headline = StringField(u'introduction', validators=[Length(0, 32, message=u"length limit 32")])
    about_me = PageDownField(u"aboutme")
    submit = SubmitField(u"submit")


class AvatarEditForm(FlaskForm):
    avatar_url = StringField('', validators=[Length(1, 100, message=u"length limt 100"), URL(message=u"please put in correct url")])
    submit = SubmitField(u"submit")


class AvatarUploadForm(FlaskForm):
    avatar = FileField('', validators=[FileAllowed(avatars, message=u"only image allowed")])
