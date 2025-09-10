from flask import Flask, request, render_template
import RegresionLinear

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index2.html")

@app.route("/conceptos")
def conceptos():
    return render_template("conceptos.html")

@app.route("/practico", methods=["GET", "POST"])
def practico():
    result = None
    if request.method == "POST":
        experiencia = float(request.form["experiencia"])
        educacion = float(request.form["educacion"])
        result = RegresionLinear.predict_salary(experiencia, educacion)
    return render_template("practico.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
