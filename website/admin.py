from flask import Blueprint, render_template, flash, send_from_directory, redirect, jsonify, url_for, request
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm, UserRoleForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer
from . import db
import json
import os
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route("/admin")
def hey():
    return 'Access Denied'

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('media/', filename)

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1 or current_user.is_admin:
        form = ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            description = form.description.data

            file = form.product_image.data
            file_name = secure_filename(file.filename)
            file_path = f'/home/rindfleisch/mysite/website/static/media/{file_name}'
            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale
            new_shop_item.description = description
            new_shop_item.product_image = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} has been added successfully')
                print(f'{product_name} has been added, the file at {file_path}')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                print(e)
                flash('Product Not Added!')
        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')

@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1 or current_user.is_admin:
        items = Product.query.order_by(Product.date_added).all()

        return render_template('shop_items.html', items=items)
    return render_template('404.html')

@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1 or current_user.is_admin:
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}
        form.description.render_kw = {'placeholder': item_to_update.description}

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            description = form.description.data

            file = form.product_image.data
            file_name = secure_filename(file.filename)
            file_path = f'/home/rindfleisch/mysite/website/static/media/{file_name}'
            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                description=description,
                                                                product_image=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Update')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1 or current_user.is_admin:
        try:
            item_to_delete = Product.query.get(item_id)
            if not item_to_delete:
                flash('Item not found')
                return redirect(url_for('admin.shop_items'))

            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item deleted successfully')
        except Exception as e:
            db.session.rollback()
            print('Item not deleted', e)
            flash(f'An error occurred while trying to delete the item {item_to_delete.product_name}')
        return redirect(url_for('admin.shop_items'))
    return render_template('404.html'), 404

"""
@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1 or current_user.is_admin:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/shop-items')
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/shop-items')

    return render_template('404.html')
    """


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1 or current_user.is_admin:
        orders = Order.query.all()
        # Combine orders with their respective customers using list comprehension
        orders_with_customers = [(order, Customer.query.get(order.customer_id)) for order in orders]
        return render_template('view_orders.html', orders_with_customers=orders_with_customers)
        """
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
        """
    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1 or current_user.is_admin:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view-orders')

        return render_template('order_update.html', form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1 or current_user.is_admin:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')

@admin.route('/update-role/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_permission(user_id):
    if current_user.id == 1 or current_user.is_admin:
        form = UserRoleForm()

        user_to_update = Customer.query.get(user_id)

        form.is_admin.render_kw = {'placeholder': user_to_update.is_admin}

        if form.validate_on_submit():
            is_admin = form.is_admin.data
            try:
                Customer.query.filter_by(id=user_id).update(dict(is_admin=is_admin))
                db.session.commit()
                if is_admin == True:
                    flash('User obtained root successfully')
                else:
                    flash('User relinquished root privileges.')
                print('Roles Upadted')
                return redirect('/customers')
            except Exception as e:
                print('User not update', e)
                flash('You must run on sudo at root!!!')

        return render_template('customer_permissions.html', form=form)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1 or current_user.is_admin:
        from datetime import datetime, timezone
        current_datetime = datetime.now(timezone.utc)
        local_datetime = current_datetime.astimezone()
        date_str = local_datetime.strftime("%B %d, %Y")  # June 21, 2024
        week_str = local_datetime.strftime("%a")  # Fri (weekday abbreviation)

        date = date_str
        week = week_str
        return render_template('admin.html', date=date, week=week)
    return render_template('404.html')

"""
JSON_FILE_PATH = '/home//mysite/website/todos.json'

def get_notes():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(notes, f, indent=4)

@admin.route('/post-notes', methods=['POST'])
@login_required
def post_notes():
    try:
        data = request.json
        if not data or 'note' not in data:
            return jsonify({"error": "Invalid input"}), 400

        notes = get_notes()
        new_id = max(note["id"] for note in notes) + 1 if notes else 1
        new_note = {
            "id": new_id,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "note": data['note']
        }

        notes.append(new_note)
        save_notes(notes)

        return jsonify({"message": "Note added successfully", "note": new_note}), 201
    except Exception as e:
        admin.logger.error(f"Error in post_notes: {e}")
        return jsonify({"error": str(e)}), 500
        """

JSON_FILE_PATH = '/home/rindfleisch/mysite/website/todos.json'

def get_notes():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(notes, f, indent=4)

@admin.route('/post-notes', methods=['POST'])
@login_required
def post_notes():
    try:
        data = request.json
        if not data or 'note' not in data:
            return jsonify({"error": "Invalid input"}), 400

        notes = get_notes()
        new_id = max(note["id"] for note in notes) + 1 if notes else 1
        new_note = {
            "id": new_id,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "note": data['note']
        }

        notes.append(new_note)
        save_notes(notes)

        return jsonify({"message": "Note added successfully", "note": new_note}), 201
    except Exception as e:
        app.logger.error(f"Error in post_notes: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route('/get-notes', methods=['GET'])
@login_required
def get_notes_route():
    try:
        notes = get_notes()
        return jsonify(notes), 200
    except Exception as e:
        app.logger.error(f"Error in get_notes_route: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route('/data-analysis')
@login_required
def data_analysis():
    if current_user.id == 1 or current_user.is_admin:
        return render_template('dataAnalysis/dataAnalysis.html')
    return render_template('404.html')

@admin.route('/api/view-data')
@login_required
def data_analysis_api():
    if current_user.id == 1 or current_user.is_admin:
        most_expensive_products = Product.query.order_by(Product.current_price.desc()).limit(5).all()
        cheap_products = Product.query.order_by(Product.current_price.asc()).limit(5).all()
        most_liked = Product.query.order_by(Product.likeness_points.desc()).limit(10).all()
        highest_stock = Product.query.order_by(Product.in_stock.desc()).limit(10).all()
        lowest_stock = Product.query.order_by(Product.in_stock.asc()).limit(10).all()
        orders = Order.query.all()
        customer_spending = {}
        for order in orders:
            if order.customer_id in customer_spending:
                customer_spending[order.customer_id] += order.quantity * order.price
            else:
                customer_spending[order.customer_id] = order.quantity * order.price
        top_spenders = sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)[:5]
        top_spenders_data = [{'name': Customer.query.get(customer_id).username, 'total_spent': total_spent} for customer_id, total_spent in top_spenders]
        data = {
            'most_expensive': [{'name': p.product_name, 'price': p.current_price} for p in most_expensive_products],
            'cheap_products': [{'name': p.product_name, 'price': p.current_price} for p in cheap_products],
            'most_liked': [{'name': p.product_name, 'points': p.likeness_points} for p in most_liked],
            'highest_stock': [{'name': p.product_name, 'stock': p.in_stock} for p in highest_stock],
            'lowest_stock': [{'name': p.product_name, 'stock': p.in_stock} for p in lowest_stock],
            'top_spenders': top_spenders_data
        }
        return jsonify(data)
    return jsonify({'error': 'Unauthorized access'}), 403