from flask import Blueprint, render_template, flash, redirect, request, jsonify, current_app, url_for
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

import random
import string
import json

DELIVERY_FEE = 50

views = Blueprint('views', __name__)

@views.route('/')
def index():
    all_items = Product.query.all()
    return render_template('home.html', all_items=all_items)

@views.route('/menu')
def view_menu():
    items = Product.query.filter_by(flash_sale=True)
    beloved_items = Product.query.order_by(Product.likeness_points.desc()).all()
    # NOTE: item all query, category
    all_items = Product.query.all()
    return render_template('menu.html', beloved_items=beloved_items ,all_items=all_items, items=items, cart=Cart.query.filter_by(customer_id=current_user.id).all() if current_user.is_authenticated else [])

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_id=item_id, customer_id=current_user.id).filter(item_to_add.in_stock > 1).first()
    if item_exists:
        try:
            if item_exists.quantity < item_to_add.in_stock:
                item_exists.quantity = item_exists.quantity + 1
                db.session.commit()
                flash(f'Quantity of { item_exists.Product.product_name } has been updated')
        except Exception as e:
            print('Quantity not updated', e)
            flash(f'Quantity of { item_exists.Product.product_name } not updated')
            return redirect(request.referrer)

    # NOTE: Adding something in models.py thingy
    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_id = item_to_add.id
    new_cart_item.customer_id = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.Product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.Product.product_name} has not been added to cart')

    return redirect(request.referrer)

@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_id=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.Product.current_price * item.quantity
    return render_template('cart.html', cart=cart,  amount=amount, total=amount+DELIVERY_FEE)

@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)

        # Fetch the actual product to get the stock limit
        product = Product.query.get(cart_item.product_id)

        # Check if the new quantity would exceed the stock limit
        if cart_item.quantity + 1 > product.in_stock:
            return jsonify({'success': False, 'message': 'Item Limit reached!'})

        cart_item.quantity += 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_id=current_user.id).all()
        amount = sum(item.Product.current_price * item.quantity for item in cart)

        data = {
            'success': True,
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + DELIVERY_FEE
        }
        return jsonify(data)

@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)

        # Check if the new quantity would be less than 1
        if cart_item.quantity - 1 < 1:
            return jsonify({'success': False, 'message': 'Quantity cannot be less than 1'})

        cart_item.quantity -= 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_id=current_user.id).all()
        amount = sum(item.Product.current_price * item.quantity for item in cart)

        data = {
            'success': True,
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 60
        }
        return jsonify(data)


@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)

        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_id=current_user.id).all()
        amount = 0

        for item in cart:
            amount += item.Product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + DELIVERY_FEE
        }
        return jsonify(data)


@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_id=current_user.id).options(joinedload('Product')).with_for_update().all()

    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                if item.Product.in_stock < item.quantity:
                    flash(f'Not enough stock for {item.Product.product_name}')
                    return redirect(url_for('views.show_cart'))
                total += item.Product.current_price * item.quantity

            characters = string.digits + string.ascii_uppercase
            random_id = ''.join(random.choice(characters) for _ in range(10))

            for item in customer_cart:
                product = Product.query.get(item.product_id)
                if product.in_stock < item.quantity:
                    flash(f'Not enough stock for {product.product_name}')
                    return redirect(url_for('views.show_cart'))

                new_order = Order(
                    quantity=item.quantity,
                    price=item.Product.current_price,
                    status='Accepted',
                    payment_id=random_id,
                    product_id=item.product_id,
                    customer_id=item.customer_id
                )
                db.session.add(new_order)

                product.in_stock -= item.quantity
                if product.in_stock < 0:
                    raise IntegrityError("Insufficient stock", "Stock reduction", "error")
                db.session.delete(item)

            db.session.commit()
            flash('Order Placed Successfully')
            return redirect(url_for('views.order'))
        except IntegrityError:
            db.session.rollback()
            flash('Order not placed due to stock issue')
            return redirect(url_for('views.show_cart'))
        except Exception as e:
            db.session.rollback()
            print(f'\n\n{e}\n\n')
            flash('Order not placed')
            return redirect(url_for('views.show_cart'))
    else:
        flash('Your cart is Empty')
        return redirect(url_for('views.show_cart'))

@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_id=current_user.id).all()
    return render_template('orders.html', orders=orders)

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_id=current_user.id).all()
                               if current_user.is_authenticated else [])
    return render_template('search.html')


cached_menu = None
with open('/home/rindfleisch/mysite/website/sml.json', 'r') as f:
    data = json.load(f)

@views.route('/chat', methods=['POST'])
def rindfleisch_chan():
    global cached_menu

    if cached_menu is None:
        all_items = Product.query.with_entities(Product.product_name, Product.current_price).all()
        cached_menu = [(item.product_name, item.current_price) for item in all_items]

    user_input = request.json.get('message').strip().lower()
    if user_input == "menu":
        return jsonify({"answer": cached_menu})
    else:
        response = data.get(user_input, "Sorry, I don't have an answer for that.")
        return jsonify({"answer": response})

@views.route('/add-likeness-points')
@login_required
def add_lpoints():
    if request.method == 'GET':
        product_id = request.args.get('product_id')

        current_app.logger.debug(f'Received product_id: {product_id}')

        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400

        product_item = Product.query.get(product_id)

        current_app.logger.debug(f'Fetched product_item: {product_item}')

        if product_item is None:
            return jsonify({'error': 'Product item not found'}), 404

        product_item.likeness_points = product_item.likeness_points + 1
        db.session.commit()

        data = {
            'likenessPoints': product_item.likeness_points
        }
        return jsonify(data)