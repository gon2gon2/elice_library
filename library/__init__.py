from flask import Flask, request,jsonify, render_template, session, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import date, timedelta
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from .models import User, Book, Rental

    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = "hahaha"

    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    
        

    @app.route('/', methods=['GET'])
    def home():
        # 세션이 없는 경우: login 페이지로 이동
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        #  세션이 있으면 메인페이지로 이동
        else:
            return redirect(url_for('mainpage'))

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
        
    @app.route('/mainpage', methods=["POST","GET"])
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
    
    @app.route('/book_return', methods=['GET'])
    def rent_book():
        
        return 
    
    @app.route('/book_return/<int:book_id>', methods=['POST'])
    def rented_books():
        return
        
        
    @app.route('/rent/<int:book_id>', methods=['GET'])
    def rent(book_id):
        book = Book.query.filter(Book.id == book_id).first()
        if book.stock <= 0:
            flash("대여하실 수 없습니다.")
            return redirect(url_for('mainpage'))
        else:
            
            start_date = date.today()
            end_date = start_date + timedelta(10)
            ### rental에 데이터 추가
            log = Rental(
                user_id = session['user_id'],
                book_id = book_id,
                start_date = date.today(),
                end_date = end_date
            )
            book.stock = book.stock - 1
            db.session.add(log)
            db.session.commit()
            
            return redirect(url_for('mainpage'))
            
            
            
            
            
            
            
            
    @app.route('/init', methods=['GET', 'POST'])
    def init_data():
        if request.method == "GET":
            return render_template('init.html')
        
        elif request.method == "POST":
            account = request.form['account']
            password = request.form['password']
            if (account == "root") & (password =="1234"):
                import csv
                from datetime import datetime

                with open('books.csv', 'r') as f:
                    reader = csv.DictReader(f)

                    for row in reader:
                        published_at = datetime.strptime(
                                        row['publication_date'], '%Y-%m-%d').date()
                        image_path = f"/static/image/{row['id']}"
                        try:
                            open(f'app/{image_path}.png')
                            image_path += '.png'
                        except:
                            image_path += '.jpg'

                        book = Book(
                            id=int(row['id']), 
                                        book_name=row['book_name'], 
                                        publisher=row['publisher'],
                            author=row['author'], 
                                        published_at=published_at, 
                                        pages=int(row['pages']),
                            isbn=row['isbn'], 
                                        description=row['description'], 
                                        image_path=image_path,
                            stock=5,
                                        rating=0,
                        )
                        db.session.add(book)

                    db.session.commit()
                return "success"
         
    @app.route('/c')
    def clear():
        books = Book.query.all()
        for book in books:
            book.stock = 5
        db.session.commit()
        return redirect(url_for('mainpage'))

    return app