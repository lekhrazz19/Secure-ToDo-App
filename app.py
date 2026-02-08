from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Needed for flash messages and sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Simple SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- SESSION SECURITY ---
app.config['SESSION_COOKIE_HTTPONLY'] = True # JavaScript cannot access the cookie (Mitigates XSS)
app.config['SESSION_COOKIE_SECURE'] = False # Set to True in production (requires HTTPS)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Protects against CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # 30 minutes timeout

db = SQLAlchemy(app)

# --- Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Where to send users who aren't logged in

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- User Model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email removed
    password_hash = db.Column(db.String(128))
    todos = db.relationship('Todo', backref='author', lazy=True)

    def set_password(self, password):
        """Hashes the password before saving."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if a password matches the hash."""
        return check_password_hash(self.password_hash, password)

# --- Todo Model ---
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200)) # Optional
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('todos'))
    return render_template('index.html')

@app.route('/todos', methods=['GET', 'POST'])
@login_required # Must be logged in
def todos():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Title is required!', 'error')
        elif len(title) > 100:
            flash('Title must be under 100 characters!', 'error')
        elif description and len(description) > 200:
            flash('Description must be under 200 characters!', 'error')
        else:
            new_todo = Todo(title=title, description=description, author=current_user)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added successfully!', 'success')
            return redirect(url_for('todos'))

    # Only show todos belonging to the current user
    user_todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', todos=user_todos)

@app.route('/update/<int:todo_id>')
@login_required
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        flash('Todo not found.', 'error')
        return redirect(url_for('todos'))
        
    # Security Check: Ensure todo belongs to current user
    if todo.user_id != current_user.id:
        flash('You do not have permission to modify this todo.', 'error')
        return redirect(url_for('todos'))
        
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('todos'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        flash('Todo not found.', 'error')
        return redirect(url_for('todos'))

    # Security Check: Ensure todo belongs to current user
    if todo.user_id != current_user.id:
        flash('You do not have permission to delete this todo.', 'error')
        return redirect(url_for('todos'))
        
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted.', 'success')
    return redirect(url_for('todos'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 2. Validate input
        if not username or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        # --- PASSWORD STRENGTH CHECK ---
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('register'))
            
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', 'error')
            return redirect(url_for('register'))
            
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'error')
            return redirect(url_for('register'))
        # -------------------------------
        
        # 3. Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        # 4. Create new user & Hash password
        new_user = User(username=username) # Removed email
        new_user.set_password(password)
        
        # 5. Save to DB
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login')) # Corrected redirect based on feedback

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check username and password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required # Cannot logout if not logged in
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.after_request
def add_security_headers(response):
    # 1. Protect against clickjacking (embedding site in an iframe)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # 2. Protect against MIME sniffing (browser guessing file types)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # 3. Enforce HTTPS (browsers remember to only use HTTPS for 1 year)
    # Note: This might break localhost if not running HTTPS, but good to learn.
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # 4. Control what the browser/referer sends
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# Create DB tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
