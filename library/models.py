from . import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    book_name = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    def __init__(self, id, book_name, publisher, author, published_at, pages, isbn, description, image_path, stock, rating):
        self.id = id
        self.book_name = book_name
        self.publisher = publisher
        self.author = author
        self.published_at = published_at
        self.pages = pages
        self.isbn = isbn
        self.description = description
        self.image_path = image_path
        self.stock = stock
        self.rating = rating
        
    
    def to_dict(self):
        result = {
            'id' : self.id,
            'book_name' : self.book_name,
            'publisher' : self.publisher,
            'author': self.author,
            'published_at': self.published_at,
            'pages': self.pages,
            'isbn': self.isbn,
            'description' : self.description,
            'image_path': self.image_path,
            'stock': self.stock,
            'rating': self.rating
        }
        return result
    
    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        


class Rental(db.Model):
    __tablename__ = "rental"
    
    # id: 대여기록 고유 id
    # start : 대여 시작일
    # end: 대여 종료일
    # user_id : 빌리는 사람 id
    # book_id : book테이블의 id
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id  = db.Column(db.Integer, db.ForeignKey('book.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    
    def __init__(self, user_id, book_id, start_date, end_date):
        self.user_id = user_id
        self.book_id = book_id
        self.start_date = start_date
        self.end_date = end_date