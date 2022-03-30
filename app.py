import json
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbweek0

app = Flask(__name__)

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