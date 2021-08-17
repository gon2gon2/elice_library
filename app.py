from flask import Flask, request,jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models.userModel import User
# from flask_migrate import Migrate
import sqlite3


app = Flask(__name__)
app.secret_key = "hahaha"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')



@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']
    
    user = User.query.filter(User.email==email).first()
    
    if password == user.password:
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('home'))
    else:
        return jsonify({'status': "fail"})



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
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
        
        return render_template('index.html')
    
    
# if __name__ == "__main__":
#     app.secret_key = "hahaha"
#     app.run(debug=True)