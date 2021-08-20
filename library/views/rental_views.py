from flask import Blueprint, request, session, render_template, redirect,url_for, jsonify, flash
from datetime import date, timedelta


from library.models import Book, BookSchema, Rental, RentalSchema
from library import db

bp = Blueprint('rental', __name__)

bookSchema = BookSchema()
rentalSchema = RentalSchema()

#  대여한 책 목록
# 다 하고 메인페이지 href 수정
@bp.route('/rented_books', methods=['GET'])
def rented():
    # 유저 id로 대여기록에 쿼리를 날린다
    # 대여기록 쿼리에서 
    user_id = session['user_id']
    rented_books = Rental.query.filter(Rental.user_id == user_id).all()

    result = []
    for book in rented_books:
        result.append(rentalSchema.dump(book))
        
    return jsonify(result)
    
#  대여하기
@bp.route('/rent/<int:book_id>', methods=['GET'])
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
        
#  반납하기
@bp.route('/book_return/<int:book_id>', methods=['POST'])
def rented_books():
    return        