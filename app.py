from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def home():
    name = "Flask"
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index2.html')

@app.route('/casos')
def casos():
    CASES = [
        {
            "titulo": "Juan ",
            "empresa": "",
            "problema": " ",
            "algoritmo": " ",
            "beneficios": " ",
            "referencia": " "
        }
,
        {
            "titulo": "Cristhian Felipe Bolivar Narvaez - Industria Bancaria ",
            "empresa": "PayPal",
            "problema": "Dado que PayPal procesa miles de millones de operaciones la repsuesta tiene que ser casi inmediata, teniendo problemas al bloquear transacciones legitimas por error; Tambien los atacantes rotan cuentas, usan bots y redes de cuentas. ",
            "algoritmo": "los algoritmos usados fueron:\n Graph analytics para detectar redes de cuentas y las relaciones,ayudando por medio de los grafos a descubrir el fraude.\n Deep learning: PayPal usa este algoritmo para explotar grandes volumenes y señales heterogeneas ya que este logra capturar patrones complejos que modelos tradicionales no pueden. ",
            "beneficios": "Gracias a los algoritmos mejora la tasa de autorizacion , detecta mejor el fraude y reduce costos de operacion ",
            "referencia": "Zuo, Q., Murthy, S., & Sharma, N. (2021, 26 de octubre). Machine Learning Model CI/CD and Shadow Platform. PayPal Technology Blog. Medium. Recuperado de https://medium.com/paypal-tech/machine-learning-model-ci-cd-and-shadow-platform-8c4f44998c78 \n OpenAI. (2025, septiembre 3). Respuesta a consulta sobre detección de fraudes en transacciones en PayPal [ChatGPT]. ChatGPT. https://chat.openai.com/ "
        }
,
        {
            "titulo": " German",
            "empresa": "",
            "problema": " ",
            "algoritmo": " ",
            "beneficios": " ",
            "referencia": " "
        },
        {
            "titulo": " Andres",
            "empresa": "",
            "problema": " ",
            "algoritmo": " ",
            "beneficios": " ",
            "referencia": " "
        }


    ]
    return render_template('index3.html', cases=CASES)

if __name__ == "__main__":
    app.run(debug=True)