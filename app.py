import json
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import hashlib
import jwt
import datetime

client = MongoClient('localhost',27017)
db = client.dbweek0

app = Flask(__name__)


# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
# db = client.dblogin

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
# 1. 도시 조회(GET)
@app.route('/read', methods=['GET'])
def read():
    cities = list(db.mytype.find({},{'_id': False}))    
    return jsonify({'result':'success', 'cities':cities})

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

# 2. 좋아요(POST)
@app.route('/like', methods=['post'])
def like():    
    cityName = request.form['city']
    city = db.mytype.find_one({'city': cityName})
    new_like = city['like']+1
    db.mytype.update_one({'city':cityName}, {'$set' : {'like' : new_like}})
    return jsonify({'result':"success"})

# 초기 데이터 불러오기
def setData():
    db.mytype.drop()
    datas = [
        {
            'id' : 1, 
            'city' : '단양',
            'image' : './static/단양.jpg',
            'desc' : "예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 ",
            'like' : 0,
            'type' : 'D'
        },
        {
            'id' : 2, 
            'city' : '포항',
            'image' : './static/포항.jpg',
            'desc' : "예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 예쁘다 ",
            'like' : 0,
            'type' : 'C'
        },
        {
            'id' : 3, 
            'city' : '제주도',
            'image' : './static/제주도.jpg',
            'desc' : "은갈치 은갈치 은갈치 은갈치 은갈치 은갈치 은갈치 예쁘다 ",
            'like' : 0,
            'type' : 'C'
        },
        {
            'id' : 4, 
            'city' : '강릉',
            'image' : './static/강릉.jpg',
            'desc' : "가지마 가지마 가지마 가지마 가지마 가지마 가지마 가지마",
            'like' : 0,
            'type' : 'B'
        },
        {
            'id' : 5, 
            'city' : '여수',
            'image' : './static/여수.jpg',
            'desc' : "엑스포 엑스포 엑스포 엑스포 엑스포 엑스포 엑스포 엑스포",
            'like' : 0,
            'type' : 'E'
        } ,
         {
            'id' : 6, 
            'city' : '광안리',
            'image' : './static/광안리.jpg',
            'desc' : "갈매기 갈매기 갈매기 갈매기 갈매기 갈매기 갈매기 갈매기 갈매기",
            'like' : 0,
            'type' : 'C'
        }      
    ]   
    for data in datas :
        db.mytype.insert_one(data)
    print("데이터 삽입 완료")    
setData()

if __name__ == "__main__":
    app.run('0.0.0.0',port=5000, debug=True)