from app import db
from app.models import User, Permission, Investment
from flask import render_template, request, flash
from flask_login import current_user
from . import main

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        amount = request.form.get('amountInput')
        strategies_list = request.form.getlist('strategiesSelect')
        strategies = ""
        for i in range(len(strategies_list)):
            if i == 0:
                strategies = strategies_list[0]
            else:
                strategies += "," + strategies_list[i]

        print("test======", amount, strategies)
        new_investment = Investment(
            user=current_user,
            amount=amount,
            strategies=strategies
            )
        db.session.add(new_investment)
        db.session.commit()
        flash(u'investment %s already added!' % new_investment.id, 'success')
        return render_template("index.html")




