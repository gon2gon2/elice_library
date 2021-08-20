from flask import Blueprint, request, session, render_template, redirect,url_for,jsonify

from library.models import Book, BookSchema
from library import db

bp = Blueprint('book', __name__)

bookSchema = BookSchema()

@bp.route('/mainpage', methods=["POST","GET"])
def mainpage():
    
    books = Book.query.all()
    result = []
    for book in books:
        result.append(bookSchema.dump(book))
    
    return render_template('mainpage.html', contents=result)

@bp.route('/detail/<int:book_id>', methods=['GET', 'POST'])
def detail(book_id):
    if request.method == 'GET':
        book = Book.query.filter(Book.id == book_id).first()
        return render_template('detail.html', content=book)
    elif request.method == 'POST':
        # 댓글 달기 로직
        return 