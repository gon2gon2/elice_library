from . import db, ma

class Book(db.Model):
    __tablename__ = "BOOK"
    rental = db.relationship('Rental', backref="BOOK")
    reply = db.relationship('Reply', backref="BOOK")
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    book_name = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
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
        
class User(db.Model):
    __tablename__ = "USER"
    rental = db.relationship('Rental')
    reply = db.relationship('Reply', backref="USER")
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

class Rental(db.Model):
    __tablename__ = "RENTAL"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    book_id  = db.Column(db.Integer, db.ForeignKey('BOOK.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    
    
    
    def __init__(self, user_id, book_id, start_date, end_date):
        self.user_id = user_id
        self.book_id = book_id
        self.start_date = start_date
        self.end_date = end_date
   
class Reply(db.Model):
    __tablename__ = "REPLY"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    book_id  = db.Column(db.Integer, db.ForeignKey('BOOK.id')) # 책
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id')) # 작성자
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.Text, nullable=False)
    
    def __init__(self, user_id, book_id, comment):
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        # self.rating = rating
   
   
   
# 30분 
# 쿼리작성 
# JSON error
# marshmallow로 해야겠다.
class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        fields = (
            'id',
            'book_name',
            'publisher',
            'author',
            'published_at',
            'pages',
            'isbn',
            'description',
            'image_path',
            'stock',
            'rating',
            )

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'name',
        )
    
class RentalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Rental
        include_fk = True
        fields = (
            'id',
            'user_id',
            'book_id',
            'start_date',
            'end_date',
        )
