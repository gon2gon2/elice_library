from db_connect import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = "rental"
    
    # id: 대여기록 고유 id
    # start : 대여 시작일
    # end: 대여 종료일
    # user_id : 빌리는 사람 id
    # book_id : book테이블의 id
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)