from flask import Flask, render_template, request
import RegresionLinear as RegresionLinear
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import io
import base64
import RegresionLogistica as Rl
import adaBoostModel

app = Flask(__name__)

@app.route("/")
def home():
    name = "Flask"
    return render_template('portada.html')

@app.route('/index2')
def index():
    return render_template('index2.html')

@app.route('/casos')
def casos():
    CASES = [
        {
            "titulo": "Juan Jose Barrera Zamora - Industria Musical",
            "empresa": "Spotify – The Echo Nest",
            "problema": "Los usuarios tienen dificultades para descubrir nueva música personalizada en medio de millones de canciones disponibles. Filtrar manualmente se vuelve imposible sin una recomendación inteligente.",
            "algoritmo": "Filtrado colaborativo, filtrado basado en contenido, técnicas de matrix factorization, NLP y modelos de audio.",
            "beneficios": "Recomendaciones personalizadas como Discover Weekly, mayor fidelización, descubrimiento de nuevos artistas, mejora en la interacción del usuario.",
            "referencia": [
                "Wikipedia. (2023, septiembre 27). The Echo Nest. En Wikipedia. https://en.wikipedia.org/wiki/The_Echo_Nest",
                "Music Machinery. (2009, mayo 19). Spotify + Echo Nest = w00t! Music Machinery. https://musicmachinery.com/2009/05/19/spotify-echo-nest-w00t/",
                "Springer. (2019). Effects of recommendations on the playlist creation behavior of users. User Modeling and User-Adapted Interaction, 29(2), 193–232. https://doi.org/10.1007/s11257-019-09237-4",
                "Wired. (2017, octubre). Musica Globalista: Spotify Discovery Engine. Wired. https://www.wired.com/beyond-the-beyond/2017/10/musica-globalista-spotify-discovery-engine",
                "Spotify. (s. f.). Understanding recommendations. Spotify. https://www.spotify.com/us/safetyandprivacy/understanding-recommendations"
            ]
        },
        {
            "titulo": "Cristhian Felipe Bolivar Narvaez - Industria Bancaria ",
            "empresa": "PayPal",
            "problema": "Dado que PayPal procesa miles de millones de operaciones la repsuesta tiene que ser casi inmediata, teniendo problemas al bloquear transacciones legitimas por error; Tambien los atacantes rotan cuentas, usan bots y redes de cuentas. ",
            "algoritmo": "los algoritmos usados fueron:\n Graph analytics para detectar redes de cuentas y las relaciones,ayudando por medio de los grafos a descubrir el fraude.\n Deep learning: PayPal usa este algoritmo para explotar grandes volumenes y señales heterogeneas ya que este logra capturar patrones complejos que modelos tradicionales no pueden. ",
            "beneficios": "Gracias a los algoritmos mejora la tasa de autorizacion , detecta mejor el fraude y reduce costos de operacion ",
            "referencia": "Zuo, Q., Murthy, S., & Sharma, N. (2021, 26 de octubre). Machine Learning Model CI/CD and Shadow Platform. PayPal Technology Blog. Medium. Recuperado de [https://medium.com/paypal-tech/machine-learning-model-ci-cd-and-shadow-platform-8c4f44998c78](https://medium.com/paypal-tech/machine-learning-model-ci-cd-and-shadow-platform-8c4f44998c78) \n OpenAI. (2025, septiembre 3). Respuesta a consulta sobre detección de fraudes en transacciones en PayPal [ChatGPT]. ChatGPT. [https://chat.openai.com/](https://chat.openai.com/) "
        },
        {
            "titulo": "German Adolfo Bautista Corena - Industria de entretenimiento",
            "empresa": "Netflix",
            "problema": "Netflix debía invertir grandes sumas en producciones originales sin certeza de éxito. Antes de apostar por una serie o película, surgían preguntas clave: ¿habrá suficiente audiencia?, ¿en qué países funcionará mejor?, ¿qué actores, directores o géneros garantizan más atractivo? Tradicionalmente los estudios se guiaban por intuición o tendencias generales, pero Netflix buscaba un enfoque más científico y escalable.",
            "algoritmo": "A finales de los 2000, con grandes volúmenes de datos de usuarios, Netflix implementó Machine Learning supervisado para predecir demanda. Usaba como entradas género, elenco, director, país, año y desempeño de títulos similares, y como salida métricas de éxito como horas vistas y nuevos suscriptores. Empleó regresión para estimar audiencias, (árboles de decisión y Random Forest) para clasificar probabilidades de éxito por segmentos, y luego (redes neuronales) para captar patrones más complejos.",
            "beneficios": "El uso de Machine Learning permitió a Netflix reducir el riesgo en sus inversiones al basarse en predicciones sustentadas en datos y no solo en la intuición, lo que facilitó acertar en mercados internacionales al anticipar qué producciones tendrían mayor éxito en regiones como Latinoamérica, Europa o Asia. Además, impulsó la expansión de su catálogo original, convirtiéndose en un valor diferencial de la plataforma, y le otorgó una ventaja competitiva frente a otros estudios que dudaban, al apostar con mayor seguridad en proyectos respaldados por modelos predictivos. ",
            "referencia": "OpenAI. (2025). Casos relevantes de Netflix y Machine Learning: problemas y algoritmos. ChatGPT (versión GPT-5) [Modelo de lenguaje]. [https://chat.openai.com/](https://chat.openai.com/), Wired. (2018, enero 2). How do Netflix’s algorithms work? Machine learning helps to predict what viewers will like. WIRED. [https://www.wired.com/story/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like](https://www.wired.com/story/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like), Netflix Technology Blog. (2018, mayo 9). Supporting content decision makers with machine learning. Medium. https://netflixtechblog.com/supporting-content-decision-makers-with-machine-learning-995b7b76006f"
        },
        {
            "titulo": "Andres Julian Canasto Acevedo, Industria Financiera",
            "empresa": "American Express",
            "problema": " American Express procesa miles de millones de transacciones anualmente, lo que representa un reto enorme en términos de seguridad financiera. El principal problema que enfrentaba la compañía era la detección de fraudes en tiempo real, ya que debía identificar operaciones sospechosas sin afectar la experiencia de los clientes legítimos. Un sistema ineficiente podría generar falsos positivos que bloqueen compras válidas, o falsos negativos que permitan fraudes millonarios. Por ello, el reto consistía en mantener la tasa de fraude más baja de la industria, mientras se garantizaba rapidez y precisión en la autorización de cada transacción ",
            "algoritmo": " Para abordar este desafío, American Express implementó modelos de aprendizaje supervisado basados en técnicas híbridas. Entre ellas se encuentran los Gradient Boosting Machines (GBM), empleados para clasificar transacciones fraudulentas, y las redes neuronales recurrentes (RNN) con LSTM, capaces de detectar patrones anómalos en series temporales de compras. Estos modelos forman parte de la décima generación de su sistema antifraude, conocido como Gen X, que combina miles de indicadores y más de mil árboles de decisión para evaluar en tiempo real la validez de cada operación. Además, la empresa utiliza infraestructura de alto rendimiento con GPUs de NVIDIA y herramientas como TensorRT y Triton Inference Server, lo que permite ejecutar inferencias en menos de dos milisegundos",
            "beneficios": " Los resultados obtenidos han sido significativos tanto a nivel técnico como financiero. La latencia del sistema se redujo a menos de dos milisegundos, lo que permite tomar decisiones instantáneas en millones de transacciones simultáneas. En términos de eficiencia, el uso de GPUs aumentó hasta 50 veces el procesamiento en comparación con sistemas tradicionales basados en CPU. Asimismo, la precisión del modelo mejoró alrededor de un 6% en segmentos específicos, logrando detectar fraudes por un valor estimado de dos mil millones de dólares al año. Gracias a estos avances, American Express ha mantenido durante catorce años consecutivos la tasa de fraude más baja de la industria de tarjetas de crédito, consolidándose como un referente en la aplicación del aprendizaje automático supervisado para la seguridad financiera ",
            "referencia": [
                "AI to Combat Financial Fraud. NVIDIA Customer Stories. [https://www.nvidia.com/en-us/customer-stories/american-express-prevents-fraud-and-foils-cybercrime-with-nvidia-ai-solutions/?utm_source=chatgpt.com](https://www.nvidia.com/en-us/customer-stories/american-express-prevents-fraud-and-foils-cybercrime-with-nvidia-ai-solutions/?utm_source=chatgpt.com) ",
                "Mixson, E. (2021, Junio 30). 3 Ways American Express is Using AI to Stay Ahead of Disruption | AI, Data & Analytics Network. AI, Data & Analytics Network. https://www.aidataanalytics.network/data-science-ai/articles/3-ways-american-express-is-using-ai-to-stay-ahead-of-disruption?utm_source=chatgpt.com",
                "Artificial intelligence at American Express - Two current use cases - EmerJ Artificial Intelligence Research. Emerj Artificial Intelligence Research. https://emerj.com/artificial-intelligence-at-american-express/?utm_source=chatgpt.com",
                "OpenAI. (2024). Casos relevantes de American Express y Machine Learning: problemas, algoritmos y beneficios. ChatGPT (versión GPT-4) [Modelo de lenguaje]. [https://chat.openai.com/](https://chat.openai.com/)",
                "Brooks, J. AmEX’s impactful use of Machine Learning – SignalScout. https://signalscout.io/amexs-impactful-use-of-machine-learning/?utm_source=chatgpt.com",
                "DigitalDefynd, T. (2025, Agosto 25). 5 ways American Express is using AI - Case Study [2025] - DigitalDefynd. DigitalDefynd. https://digitaldefynd.com/IQ/american-express-using-ai-case-study/?utm_source=chatgpt.com",
                "American Express: Using Big Data to Prevent Fraud - Digital Innovation and Transformation. (2022, Octubre 2). Digital Innovation and Transformation. https://d3.harvard.edu/platform-digit/submission/american-express-using-big-data-to-prevent-fraud/?utm_source=chatgpt.com"
            ]
        }
    ]
    return render_template('index3.html', cases=CASES)

# ... el resto de tu código ...

@app.route("/RLconceptos")
def RLconceptos():
    return render_template("RLconceptos.html")

@app.route("/RLpractico", methods=["GET", "POST"])
def RLpractico():
    result = None
    grafico_url = None

    if request.method == "POST":
        experiencia = float(request.form["experiencia"])
        educacion = float(request.form["educacion"])

        # 🔹 Predicción
        result = RegresionLinear.predict_salary(experiencia, educacion)

        # 🔹 Crear gráficos comparativos
        plt.figure(figsize=(12, 5))

        # Subplot 1: Experiencia vs Sueldo
        plt.subplot(1, 2, 1)
        exp_range = range(0, 16)  # Experiencia de 0 a 15 años
        sueldos_exp = [RegresionLinear.model.predict([[e, educacion]])[0] for e in exp_range]

        plt.scatter(RegresionLinear.df["Experiencia"], RegresionLinear.df["Sueldo"], color="blue", label="Datos")
        plt.plot(exp_range, sueldos_exp, color="red", label=f"Corte con Educación={educacion}")
        plt.scatter(experiencia, RegresionLinear.model.predict([[experiencia, educacion]])[0],
                    color="black", marker="X", s=100, label="Tu predicción")

        plt.xlabel("Años de experiencia")
        plt.ylabel("Sueldo")
        plt.title("Experiencia vs Sueldo")
        plt.legend()
        plt.grid(True)

        # Subplot 2: Educación vs Sueldo
        plt.subplot(1, 2, 2)
        edu_range = range(1, 8)  # Niveles educativos
        sueldos_edu = [RegresionLinear.model.predict([[experiencia, e]])[0] for e in edu_range]

        plt.scatter(RegresionLinear.df["Educacion"], RegresionLinear.df["Sueldo"], color="green", label="Datos")
        plt.plot(edu_range, sueldos_edu, color="orange", label=f"Corte con Experiencia={experiencia}")
        plt.scatter(educacion, RegresionLinear.model.predict([[experiencia, educacion]])[0],
                    color="black", marker="X", s=100, label="Tu predicción")

        plt.xlabel("Nivel educativo")
        plt.ylabel("Sueldo")
        plt.title("Educación vs Sueldo")
        plt.legend()
        plt.grid(True)

        # Guardar gráfico en memoria como Base64
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        grafico_url = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()  

    return render_template("RLpractico.html", result=result, grafico_url=grafico_url)

@app.route("/LRconceptos")
def LRconceptos():
    return render_template("LRconceptos.html", title="Conceptos")


@app.route("/LRpractico", methods=["GET", "POST"])
def LRpractico():
    resultado, prob, grafico_url = None, None, None

    if request.method == "POST":
        tiempo = float(request.form["tiempo"])
        clics = int(request.form["clics"])
        fuente = request.form["fuente"]
        ingresos = request.form["ingresos"]

        prob, resultado = Rl.predecir_compra(tiempo, clics, fuente, ingresos)

    matriz_url = Rl.obtener_matriz_confusion()

    return render_template(
        "LRpractico.html",
        title="Ejercicio Práctico",
        resultado=resultado,
        prob=prob,
        grafico_url=grafico_url,
        matriz_url=matriz_url,

        
    )


@app.route("/AdaBoostConceptos")
def AdaBoostConceptos():
    return render_template("AdaBoostConceptos.html", title="Conceptos AdaBoost")

@app.route("/AdaBoostPractico", methods=["GET", "POST"])
def AdaBoostPractico():
    metrics = adaBoostModel.evaluate()
    prediction_result = None
    prediction_prob = None
    threshold = 0.5

    if request.method == "POST":
        try:
            features = {
                'Tiempo atencion': float(request.form['tiempo_atencion']),
                'Resolucion problema': int(request.form['resolucion_problema']),
                'Tono agente': request.form['tono_agente'],
                'Canal contacto': request.form['canal_contacto']
            }
            if request.form.get('threshold'):
                threshold = float(request.form['threshold'])
            prediction_result, prediction_prob = adaBoostModel.predict_label(features, threshold)
        except Exception as e:
            prediction_result = f"Error en la predicción: {str(e)}"

    return render_template(
        "AdaBoostPractico.html",
        title="Caso práctico AdaBoost",
        metrics=metrics,
        prediction_result=prediction_result,
        prediction_prob=prediction_prob,
        threshold=threshold
    )

@app.route("/RLrefuerzoConceptos", methods=["GET"])
def RLrefuerzoConceptos():
    # Puedes pasar variables a la plantilla según tu necesidad
    return render_template("RLrefuerzoConceptos.html", title="Conceptos Aprendizaje por Refuerzo")


if __name__ == "__main__":

    app.run(debug=True)

