from db_connect import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    book_name = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        result = {
            'id' : self.id,
            'book_name' : self.book_name,
            'publisher' : self.publisher,
            'author': self.author,
            'publication_date': self.publication_date,
            'pages': self.pages,
            'isbn': self.isbn,
            'description' : self.description,
            'link': self.link,
            'img':f"../data/bookcover/{str(self.id)}.png"
        }
        return result