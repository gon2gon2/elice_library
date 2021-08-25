from flask import Blueprint, request, session, render_template, redirect,url_for, jsonify, flash
from datetime import date, timedelta


from library.models import Book, Rental
from library import db

bp = Blueprint('rental', __name__)

@bp.before_request
def before_request():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

# 대여 기록
@bp.route('/rented_books', methods=['GET'])
def rented():
    user_id = session['user_id']
    rented_books = Rental.query.filter(Rental.user_id == user_id).order_by(Rental.end_date.desc()).all()
    return render_template('rented_books.html', books=rented_books)
    
#  대여하기
@bp.route('/rent_book/<int:book_id>', methods=['GET'])
def rent(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    if book.stock <= 0:
        flash("대여하실 수 없습니다.")
        return redirect(url_for('book.mainpage'))
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
        
        return redirect(url_for('book.mainpage'))
        
#  반납하기 페이지
@bp.route('/return_book', methods=['GET'])
def return_books():
    user_id = session['user_id']
    books = Rental.query.filter((Rental.returned==0) & (Rental.user_id == user_id)).all()
    
    return render_template('return_books.html', books=books)
        

#  반납기능
@bp.route('/return_book/<int:book_id>', methods=['GET'])
def rented_books(book_id):
    user_id = session['user_id']
    book_returned = Rental.query.filter((Rental.book_id==book_id) & (Rental.user_id == user_id)).first()
    book = Book.query.filter(Book.id == book_id).first()
    
    # 반납할 책을 찾아서 Rental에서 삭제
    # 날짜를 오늘로 바꾸고 returned를 True로 바꿈
    book_returned.end_date = date.today()
    book_returned.returned = True
    
    # 반납된 책의 재고를 +1
    book.stock = book.stock + 1
    
    db.session.commit()
    return redirect(url_for('rental.return_books'))