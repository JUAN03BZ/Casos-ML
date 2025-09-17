import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import RegresionLogistica as Rl  # Importar funciones del módulo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Portada")


@app.route("/home")
def home():
    return render_template("home.html", title="Inicio")


@app.route("/conceptos")
def conceptos():
    return render_template("conceptos.html", title="Conceptos")


@app.route("/practico", methods=["GET", "POST"])
def practico():
    resultado, prob, grafico_url = None, None, None

    if request.method == "POST":
        tiempo = float(request.form["tiempo"])
        clics = int(request.form["clics"])
        fuente = request.form["fuente"]
        ingresos = request.form["ingresos"]

        prob, resultado = Rl.predecir_compra(tiempo, clics, fuente, ingresos)

    matriz_url = Rl.obtener_matriz_confusion()

    return render_template(
        "practico.html",
        title="Ejercicio Práctico",
        resultado=resultado,
        prob=prob,
        grafico_url=grafico_url,
        matriz_url=matriz_url,

        
    )


if __name__ == "__main__":
    app.run(debug=True)