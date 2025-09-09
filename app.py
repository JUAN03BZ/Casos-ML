from flask import Flask, request 
from flask import render_template
import RegresionLinear

app = Flask(__name__)

@app.route('/')
def home():
    name=None
    name = "Flask"
    return f"Hello, {name}!"

@app.route('/index')
def index():
    myname = "Flask"
    return render_template('index.html', name=myname)

@app.route('/LR')
def lr():
    calculateResult = None
    #if request.method == 'POST':
    calculateResult = RegresionLinear.calculate_grade(5)
    return "Final Grade Prediction: " + str(calculateResult)

if __name__ == '__main__':
    app.run(debug=True)
