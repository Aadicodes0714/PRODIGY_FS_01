from flask import Flask, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-change-in-production'

# In-memory "database" for demo
users = {}

@app.route('/')
def index():
    return render_template('index.html', msg=request.args.get('msg'))

@app.route('/register', methods=['POST'])
def register():
    u = request.form['username']
    p = request.form['password']

    if u in users:
        return redirect(url_for('index', msg='User already exists'))

    users[u] = generate_password_hash(p)
    return redirect(url_for('index', msg='Registration successful! Please log in.'))

@app.route('/login', methods=['POST'])
def login():
    u = request.form['username']
    p = request.form['password']

    if u in users and check_password_hash(users[u], p):
        session['username'] = u
        return redirect(url_for('protected'))

    return redirect(url_for('index', msg='Invalid credentials'))

@app.route('/protected')
def protected():
    if 'username' not in session:
        return redirect(url_for('index', msg='Access denied. Please log in first.'))
    return render_template('protected.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index', msg='Logged out successfully'))

if __name__ == '__main__':
    app.run(debug=True)