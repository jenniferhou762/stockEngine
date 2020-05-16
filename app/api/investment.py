from app.models import Investment as model_Investment
from flask import url_for
from flask_restful import Resource, marshal_with, abort
from . import api, parser, default_per_page
from .fields import investment_fields, investment_list


@api.route('/investments/<int:investment_id>/')
class Investment(Resource):
    @marshal_with(investment_fields)
    def get(self, investment_id):
        investment = model_Investment.query.get_or_404(investment_id)
        # if book.hidden:
        #     abort(404)
        return investment


@api.route('/investments/')
class InvestmentList(Resource):
    @marshal_with(investment_list)
    def get(self):
        args = parser.parse_args()
        page = args['page'] or 1
        per_page = args['per_page'] or default_per_page
        pagination = model_Investment.query.paginate(page=page, per_page=per_page)
        items = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.investmentlist', page=page - 1, count=per_page, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('api.investmentlist', page=page + 1, count=per_page, _external=True)
        return {
            'items': items,
            'prev': prev,
            'next': next,
            'total': pagination.total,
            'pages_count': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
        }
