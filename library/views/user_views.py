from flask import Blueprint, request, session, render_template, redirect,url_for,jsonify

from library.models import User
from library import db

bp = Blueprint('user', __name__)

@bp.route('/', methods=['GET'])
def home():
    # 세션이 없는 경우: login 페이지로 이동
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    #  세션이 있으면 메인페이지로 이동
    else:
        return redirect(url_for('book.mainpage'))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter(User.email==email).first()
        
        if user in None:
            return "회원정보가 존재하지 않습니다!"
        
        if password != user.password:
            return "비밀번호가 일치하지 않습니다!"
        
        session.clear()
        session['user_id'] = user.id
        session['name'] = user.name
        return redirect(url_for('user.home'))
            
            
@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        
        if password != password_check:
            return "비밀번호가 일치하지 않습니다"
        
        elif User.query.filter(User.email==email).first() != None:
            return '이미 존재하는 유저입니다'
        
        user = User(
            email=email,
            password=password,
            name=name
            )
        db.session.add(user)
        db.session.commit()
        
        return render_template('login.html')
        