from flask import url_for
from flask_restful import fields
from . import default_per_page

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'major': fields.String,
    'headline': fields.String,
    'about_me': fields.String,
    'about_me_html': fields.String,
    'avatar': fields.String(attribute=lambda x: x.avatar_url(_external=True)),
    'uri': fields.String(attribute=lambda x: url_for('api.user', user_id=x.id, _external=True)),
}
user_list = {
    'items': fields.List(fields.Nested(user_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}

investment_fields = {
    'id': fields.Integer,
    'investAt': fields.DateTime(dt_format='rfc822'),
    'user_id': fields.Integer,
    'amount': fields.Integer,
    'strategies': fields.String,
    'uri': fields.String(attribute=lambda x: url_for('api.investment', investment_id=x.id, _external=True)),
}
investment_list = {
    'items': fields.List(fields.Nested(investment_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}
user_detail_fields = dict \
    (user_fields, **{

    }
     )
