from flask import Flask, render_template
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

@app.route('/myPage')
def myPage():
    return render_template('myPage.html')

if __name__ == "__main__":
    app.run('0.0.0.0',port=5000, debug=True)