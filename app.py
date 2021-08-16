from flask import Flask, request,jsonify, render_template


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    # id = requests.get
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)