from flask import Flask, render_template, redirect, flash, url_for, session,logging, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from forms import RegisterForm, ArticleForm
from dbconnect import dbconnect

# from flask_socketio import SocketIO, emit
# from flask_login import current_user, logout_user

app = Flask(__name__)
app.secret_key='secret123'
# socketio = SocketIO(app)
# mysql config

app.config['MYSQL_HOST'] = dbconnect.host
app.config['MYSQL_USER'] = dbconnect.user
app.config['MYSQL_PASSWORD'] = dbconnect.passwd
app.config['MYSQL_CURSORCLASS'] = dbconnect.cursorclass

mysql = MySQL(app)


# index
@app.route('/')
def index():
    return render_template('index.html')

#about
@app.route('/about/')
def about():
    return render_template('about.html')

# articles
@app.route('/articles')
def articles():
    
    cur = mysql.connection.cursor()
    cur.execute("USE flaskblog")
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles = articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

    cur.close()

# articles - specific
@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    cur.execute("USE flaskblog")
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])
    
    article = cur.fetchone()

    return render_template('article.html', article=article)



# User registtration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("USE flaskblog")
        cur.execute("INSERT INTO users(name,username,email,password) VALUES (%s, %s, %s, %s)", (name, username, email, password))
        mysql.connection.commit()
        cur.close()

        flash('You are now registered and Can Login', 'success')
        redirect(url_for('index'))

    return render_template('register.html', form=form) 

# UserLogin
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pass_cand = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("USE flaskblog")
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']

            # compare pass
            if sha256_crypt.verify(pass_cand, password):
                # app.logger.info("PASS MATCHE")
                session['logged_in'] = True
                session['username'] = username

                flash("You are now logged in !",'success')
                return redirect(url_for('dashboard'))
            else:
                # app.logger.info("PASS NOT MATCHED")
                error = 'Invalid Login Credentials'
                return render_template('login.html',error=error)
            cur.close()
        else:
            # app.logger.info("NO USER FOUND")
            error = 'Username not found'
            return render_template('login.html',error=error)

    return render_template('login.html')

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unathorised Please Log in','danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are Logged Out', 'primary')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()
    cur.execute("USE flaskblog")
    result = cur.execute("SELECT * FROM articles WHERE author=%s",[session=['username']])

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles = articles)
    else:
        msg = 'No aritcles Found'
        return render_template('dashboard.html', msg=msg)

    cur.close()


#add article
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("USE flaskblog")

        cur.execute("INSERT INTO articles(title,body,author) VALUES (%s, %s, %s)", (title,body,session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Article Created !', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

# edit articles
@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):

    cur = mysql.connection.cursor()
    cur.execute("USE flaskblog")
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    form = ArticleForm(request.form)
    
    #populate form
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("USE flaskblog")

        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Article Updated !', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# delete 
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("USE flaskblog")

    cur.execute("DELETE FROM articles WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Article Deleted !', 'success')

    return redirect(url_for('dashboard'))

# @socketio.on('disconnect')
# def disconnect_user():
#     session.clear()
#     # session.pop('username', None)

if __name__ == "__main__":
    app.run(debug=True)
