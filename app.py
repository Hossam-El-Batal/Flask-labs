from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import timedelta
import base64
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)
migrate = Migrate(app, db)  


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    books = db.relationship('Book', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    image = db.Column(db.LargeBinary) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

@app.route('/view_books')
@login_required
def view_books():
    user = User.query.get(session['user_id'])
    books = Book.query.filter_by(user_id=user.id).all()
    return render_template('view_books.html', books=books)

@app.route('/remove_book/<int:book_id>')
@login_required
def remove_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id == session['user_id']:
        db.session.delete(book)
        db.session.commit()
        flash('Book removed successfully!', 'success')
    else:
        flash('You do not have permission to delete this book.', 'danger')
    return redirect(url_for('view_books'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Admin access required.', 'warning')
        return redirect(url_for('index'))
    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_dashboard.html', users=users, books=books)

@app.route('/delete_account/<int:user_id>')
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if not User.query.get(session['user_id']).is_admin:
        flash('Admin access required.', 'warning')
        return redirect(url_for('index'))
    db.session.delete(user)
    db.session.commit()
    flash('User account deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('view_books'))
    return render_template('edit_book.html', book=book)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  