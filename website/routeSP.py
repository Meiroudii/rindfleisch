from flask import Blueprint, render_template, flash, redirect, request, jsonify, current_app, url_for
from .models import Product, Cart, Order
from . import db
from flask_login import login_required, current_user

routeSP = Blueprint('routeSP', __name__)

@routeSP.route('/special')
@login_required
def indexSP():
    return render_template("specialTemplates/baseSP.html")