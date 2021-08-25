from flask import Blueprint, request, session, render_template, redirect,url_for

from library.models import Book, Reply
from library import db

bp = Blueprint('book', __name__)



@bp.route('/mainpage', methods=["GET"])
def mainpage():
    books = Book.query.all()    
    return render_template('mainpage.html', books=books)

@bp.route('/detail/<int:book_id>', methods=['GET', 'POST'])
def detail(book_id):
    if request.method == 'GET':
        book = Book.query.filter(Book.id == book_id).first()
        return render_template('detail.html', book=book)
    
    elif request.method == 'POST':
        user_id = session['user_id']
        comment = request.form['comment']
        reply = Reply(
            user_id = user_id,
            book_id = book_id,
            comment = comment
        )
        db.session.add(reply)
        db.session.commit()
        return redirect(f'/detail/{book_id}')