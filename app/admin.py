# # app/admin.py

# from flask import Blueprint, render_template, redirect, url_for, session, flash
# from .models import User, Book, db

# admin_bp = Blueprint('admin', __name__)

# @admin_bp.route('/admin_dashboard')
# def admin_dashboard():
#     user = User.query.get(session['user_id'])
#     if not user.is_admin:
#         flash('Admin access required.', 'warning')
#         return redirect(url_for('books.index'))
#     users = User.query.all()
#     books = Book.query.all()
#     return render_template('admin_dashboard.html', users=users, books=books)

# @admin_bp.route('/delete_account/<int:user_id>')
# def delete_account(user_id):
#     user = User.query.get_or_404(user_id)
#     if not User.query.get(session['user_id']).is_admin:
#         flash('Admin access required.', 'warning')
#         return redirect(url_for('books.index'))
#     db.session.delete(user)
#     db.session.commit()
#     flash('User account deleted.', 'success')
#     return redirect(url_for('admin.admin_dashboard'))

# app/admin.py

from flask import Blueprint, render_template, redirect, url_for, session, flash
from .models import User, Book, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    # Ensure there's a logged-in user
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to be logged in to access the admin dashboard.', 'warning')
        return redirect(url_for('books.index'))

    user = User.query.get(user_id)
    if not user or not user.is_admin:
        flash('Admin access required.', 'warning')
        return redirect(url_for('books.index'))

    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_dashboard.html', users=users, books=books)

@admin_bp.route('/delete_account/<int:user_id>', methods=['GET'])
def delete_account(user_id):
    # Ensure there's a logged-in user
    admin_id = session.get('user_id')
    if not admin_id:
        flash('You need to be logged in to delete an account.', 'warning')
        return redirect(url_for('books.index'))

    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin:
        flash('Admin access required.', 'warning')
        return redirect(url_for('books.index'))

    user = User.query.get_or_404(user_id)
    
    # Optional: Prevent deleting the admin user if needed
    if user.id == admin.id:
        flash('You cannot delete your own account.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash('User account deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/delete_book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    admin_id = session.get('user_id')
    if not admin_id:
        flash('You need to be logged in to delete a book.', 'warning')
        return redirect(url_for('books.index'))

    admin = User.query.get(admin_id)
    if not admin or not admin.is_admin:
        flash('Admin access required.', 'warning')
        return redirect(url_for('books.index'))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))