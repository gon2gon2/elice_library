from flask import Flask, request, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    
    from .models import Book
    
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = "hahaha"

    from .views import user_views, book_views, rental_views
    app.register_blueprint(user_views.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(rental_views.bp)
    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
        
            
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