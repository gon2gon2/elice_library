

from library import app
from library import db
from library.models import Book

import csv
from datetime import date, datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'My connection string'
db.init_app(app)


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
						name=row['book_name'], 
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