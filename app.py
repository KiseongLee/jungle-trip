from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import hashlib
import jwt
import datetime
app = Flask(__name__)


client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dblogin

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/survey')
def survey():    
    return render_template('survey.html')

@app.route('/surveyResult')
def surveyResult():
    return render_template('surveyResult.html')

@app.route('/mypage')
def myPage():
    return render_template('myPage.html')

# ------ API -------

#회원가입 API

@app.route('/api/sign', methods=['POST']) 
def api_register(): 
    # 1. 클라이언트로부터 데이터 받기
    name_receive = request.form['name_give']
    id_receive = request.form['id_give'] 
    pw_receive = request.form['pwd_give'] 
     
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() 

    db.user.insert_one({'name': name_receive, 'id': id_receive, 'pw': pw_hash }) 
    
    return jsonify({'result': 'success'})

@app.route('/api/login', methods=['POST']) 
def api_login(): 

    id_receive = request.form['id_give'] 
    pw_receive = request.form['pwd_give'] 
    
    
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash}) 
    
     
    if result is not None: 
         
     payload = { 
         'id': id_receive, 
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=2400) #언제까지 유효한지 
     } 
     
     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') 
     
     return jsonify({'result': 'success', 'token': token}) 
     
    else: 
          return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

SECRET_KEY = 'secret_key'


if __name__ == "__main__":
    app.run('0.0.0.0',port=5000, debug=True)