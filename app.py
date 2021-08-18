import csv
from datetime import date, datetime

from flask import Flask, request,jsonify, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models.userModel import User
from models.bookModel import Book
from flask_migrate import Migrate



app = Flask(__name__)
app.secret_key = "hahaha"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# @app.route('/init', methods=['GET'])
# def init_data():
    

@app.route('/', methods=['GET'])
def home():
    
    # 세션이 없는 경우: login 페이지로 이동
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    #  세션이 있으면 메인페이지로 이동
    else:
        return redirect(url_for('mainpage'))

app.config['JSON_AS_ASCII'] = False

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter(User.email==email).first()
        
        if password == user.password:
            session.clear()
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('home'))
        else:
            return jsonify({'status': "fail"})
        
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        
        if password != password_check:
            return "비밀번호가 일치하지 않습니다"
        
        elif User.query.filter(User.email==email).first() != None:
            return '이미 존재하는 유저입니다'
        
        user = User(
            email=email,
            password=password,
            name=name
            )
        db.session.add(user)
        db.session.commit()
        
        return render_template('login.html')
    
@app.route('/mainpage', methods=["GET"])
def mainpage():
    books = Book.query.all()
    result = []
    for book in books:
        result.append(book.to_dict())
    
    return render_template('mainpage.html', contents=result)


@app.route('/detail/<int:book_id>', methods=['GET', 'POST'])
def detail(book_id):
    if request.method == 'GET':
        book = Book.query.filter(Book.id == book_id).first()
        return render_template('detail.html', content=book)
    elif request.method == 'POST':
        # 댓글 달기 로직
        return 
    
    
if __name__ == "__main__":
    app.secret_key = "hahaha"
    app.run(debug=True)