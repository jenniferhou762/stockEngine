# -*- coding:utf-8 -*-
from app import db
from app.models import Permission, Investment
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from . import investment
from ..decorators import admin_required, permission_required


@investment.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    current_user_id = int(current_user.get_id())
    print(current_user_id)
    the_investments = Investment.query.filter_by(user_id=current_user_id)

    pagination = the_investments.paginate(page, per_page=8)
    result_investments = pagination.items
    return render_template("investment.html", investments=result_investments, pagination=pagination, 
                           title=u"Investments")


@investment.route('/<investment_id>/')
def detail(investment_id):
    the_investment = Investment.query.get_or_404(investment_id)

    return render_template("investment_detail.html", investment=the_investment)
