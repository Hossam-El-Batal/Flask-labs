from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .models import Book, User, db
import base64
from .auth import login_required
books_bp = Blueprint('books', __name__)

@books_bp.route('/')
def index():
    return render_template('index.html')

@books_bp.route('/dashboard')
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@books_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image = request.files['image']
        if image:
            image_blob = base64.b64encode(image.read())
        else:
            image_blob = None
        book = Book(title=title, author=author, image=image_blob, user_id=session['user_id'])
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.view_books'))
    return render_template('add_book.html')

@books_bp.route('/view_books')
def view_books():
    user = User.query.get(session['user_id'])
    books = Book.query.filter_by(user_id=user.id).all()
    return render_template('view_books.html', books=books)

@books_bp.route('/remove_book/<int:book_id>')
@login_required
def remove_book(book_id):
    book = Book.query.get_or_404(book_id)
    user = User.query.get(session['user_id'])  
    if book.user_id == session['user_id'] or user.is_admin:
        db.session.delete(book)
        db.session.commit()
        flash('Book removed successfully!', 'success')
    else:
        flash('You do not have permission to delete this book.', 'danger')
    return redirect(url_for('books.view_books'))

@books_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        image = request.files['image']
        if image:
            book.image = base64.b64encode(image.read())
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.view_books'))
    return render_template('edit_book.html', book=book)
