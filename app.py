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
    
    cities = list(db.mytype.find({},{'_id': False}).sort("like", -1))    
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
            'desc' : "충청북도 단양군<br> 여행지 : 단양 도담 삼봉&석문, 고수동굴, 만천하스카이워크<br> 먹거리 : 쏘가리 매운탕, 마늘 떡갈비, 마늘치킨<br> 액티비티 : 패러글라이딩, 짚와이어, 래프팅, 루어낚시, 유람선<br>",
            'like' : 0,
            'type' : 'D'
        },
        {
            'id' : 2, 
            'city' : '포항',
            'image' : './static/포항.jpg',
            'desc' : "경상남도 포항시<br> 여행지 : 환호공원 스페이스 워크, 영일교, 호미곶 해맞이 광장<br> 먹거리 : 시락국, 대게, 과메기, 고래 고기, 모리 국수<br> 액티비티 : 호미곶ATV, 포항크루즈<br> ",
            'like' : 0,
            'type' : 'C'
        },
        {
            'id' : 3, 
            'city' : '제주도',
            'image' : './static/제주도.jpg',
            'desc' : "제주특별자치도<br> 여행지 : 성산일출봉, 한라산, 올레길, 비자림<br> 먹거리 : 흑돼지삼겹살, 고기국수, 돔베고기, 성게미역국<br> 액티비티 : 바체올린 카약, 더마파크 승마, 974 카트 테마파크<br> ",
            'like' : 0,
            'type' : 'C'
        },
        {
            'id' : 4, 
            'city' : '강릉',
            'image' : './static/강릉.jpg',
            'desc' : " 강원도 강릉시<br> 여행지 : 경포해수욕장, 오죽헌, 경포대, 정동진 해변 <br>먹거리 : 초당 두부, 감자 옹심이, 물회, 장칼국수 <br> 액티비티 : 서핑, 요트투어, 정동진 레일바이크<br>",
            'like' : 0,
            'type' : 'B'
        },
        {
            'id' : 5, 
            'city' : '여수',
            'image' : './static/여수.jpg',
            'desc' : "전라남도 여수시<br> 여행지 : 오동도, 향일암, 여수 아쿠아리움, 아이뮤지엄 미디어 포레스트<br> 먹거리 : 돌산갓김치, 게장 백반, 서대회무침<br> 액티비티 : 유월드 루지 테마파크, 라마다 여수 해상 짚트랙<br>",
            'like' : 0,
            'type' : 'E'
        } ,
         {
            'id' : 6, 
            'city' : '광안리',
            'image' : './static/광안리.jpg',
            'desc' : "부산 광역시<br> 여행지 : 해운대, 광안리, 태종대유원지, 감천문화마을<br> 먹거리 : 돼지국밥, 밀면, 제철 회, 냉채 족발, 동래파전<br> 액티비티 : 광안리 제트보트&요트투어, 패들보드, 카약, 카이트 서핑<br>",
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