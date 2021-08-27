from flask import Blueprint, request, session, render_template, redirect,url_for

from library.models import Book, Reply
from library import db

bp = Blueprint('book', __name__)

@bp.before_request
def before_request():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

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
        # 댓글 추가 로직
        user_id = session['user_id']
        comment = request.form['comment']
        rating = len(request.form.keys()) - 1

        
        reply = Reply(
            user_id = user_id,
            book_id = book_id,
            rating = rating,
            comment = comment
        )
        db.session.add(reply)
        
        # book의 rating 바꿔주는 로직
        book = Book.query.filter(Book.id == book_id).first()
        reply = book.reply
        star = []
        for r in reply:
            star.append(r.rating)
        avg = sum(star)/len(star)
        book.rating = avg
        
        
        db.session.commit()
        return redirect(f'/detail/{book_id}')