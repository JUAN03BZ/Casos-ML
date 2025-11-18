from flask import Flask, render_template, request, jsonify
import RegresionLinear as RegresionLinear
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import io
import base64
import RegresionLogistica as Rl
import adaBoostModel
import RefuerzoPractico
import os
import pickle
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

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
            "referencia": "OpenAI. (2025). Casos relevantes de Netflix y Machine Learning: problemas y algoritmos. ChatGPT (versión GPT-5) [Modelo de lenguaje]. [https://chat.openai.com/](https://chat.openai.com/), Wired. (2018, enero 2). How do Netflix's algorithms work? Machine learning helps to predict what viewers will like. WIRED. [https://www.wired.com/story/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like](https://www.wired.com/story/how-do-netflixs-algorithms-work-machine-learning-helps-to-predict-what-viewers-will-like), Netflix Technology Blog. (2018, mayo 9). Supporting content decision makers with machine learning. Medium. https://netflixtechblog.com/supporting-content-decision-makers-with-machine-learning-995b7b76006f"
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
                "Brooks, J. AmEX's impactful use of Machine Learning – SignalScout. https://signalscout.io/amexs-impactful-use-of-machine-learning/?utm_source=chatgpt.com",
                "DigitalDefynd, T. (2025, Agosto 25). 5 ways American Express is using AI - Case Study [2025] - DigitalDefynd. DigitalDefynd. https://digitaldefynd.com/IQ/american-express-using-ai-case-study/?utm_source=chatgpt.com",
                "American Express: Using Big Data to Prevent Fraud - Digital Innovation and Transformation. (2022, Octubre 2). Digital Innovation and Transformation. https://d3.harvard.edu/platform-digit/submission/american-express-using-big-data-to-prevent-fraud/?utm_source=chatgpt.com"
            ]
        }
    ]
    return render_template('index3.html', cases=CASES)

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

@app.route("/RLrefuerzoConceptos")
def RLrefuerzoConceptos():
    return render_template("RLrefuerzoConceptos.html")

@app.route("/RLrefuerzoPractico", methods=["GET", "POST"])
def RLrefuerzoPractico():
    # Parámetros por defecto
    alpha = 0.5
    gamma = 0.9
    epsilon = 0.3
    episodes = 500
    
    # Asegurar que static existe
    os.makedirs('static', exist_ok=True)
    
    # Verificar si ya existe un modelo entrenado
    trained = os.path.exists('static/rewards.png')
    tested = os.path.exists('static/trajectory.png')
    
    if request.method == "POST":
        # Aquí podrías capturar parámetros del formulario si los agregas
        alpha = float(request.form.get('alpha', alpha))
        gamma = float(request.form.get('gamma', gamma))
        epsilon = float(request.form.get('epsilon', epsilon))
        episodes = int(request.form.get('episodes', episodes))
        
        # Ejecutar entrenamiento
        try:
            # Importar y entrenar agente
            from RefuerzoPractico import GridWorldAgent
            
            agent = GridWorldAgent(alpha=alpha, gamma=gamma, epsilon=epsilon)
            episode_rewards, episode_steps = agent.train(episodes=episodes)
            
            # Generar y guardar gráficas
            agent.plot_training(episode_rewards)
            agent.save_model('static/modelo_entrenado.pkl')
            
            trained = True
            result = f"Entrenamiento completado con {episodes} episodios"
            
        except Exception as e:
            result = f"Error en el entrenamiento: {str(e)}"
    
    return render_template(
        "RLrefuerzoPractico.html",
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        episodes=episodes,
        actions=["up", "down", "left", "right"],
        trained=trained,
        tested=tested,
        timestamp=int(datetime.now().timestamp())  # Para evitar cache
    )

@app.route("/train_RL", methods=["POST"])
def train_RL():
    """Endpoint para entrenamiento asíncrono"""
    try:
        # Asegurar que la carpeta static existe
        os.makedirs('static', exist_ok=True)
        
        print("🔧 Iniciando entrenamiento...")
        
        # Parámetros del request
        data = request.get_json() or {}
        alpha = data.get('alpha', 0.5)
        gamma = data.get('gamma', 0.9)
        epsilon = data.get('epsilon', 0.3)
        episodes = data.get('episodes', 500)
        
        print(f"🔧 Parámetros: α={alpha}, γ={gamma}, ε={epsilon}, episodios={episodes}")
        
        # Importar y entrenar agente
        try:
            from RefuerzoPractico import GridWorldAgent
            print("✓ GridWorldAgent importado correctamente")
        except ImportError as e:
            print(f"✗ Error importando GridWorldAgent: {e}")
            return jsonify({
                "status": "error",
                "message": f"Error importando el agente: {str(e)}"
            }), 500
        
        try:
            agent = GridWorldAgent(alpha=alpha, gamma=gamma, epsilon=epsilon)
            print("✓ Agente creado correctamente")
            
            episode_rewards, episode_steps = agent.train(episodes=episodes)
            print(f"✓ Entrenamiento completado. Recompensa final: {episode_rewards[-1] if episode_rewards else 'N/A'}")
            
        except Exception as e:
            print(f"✗ Error durante el entrenamiento: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "status": "error", 
                "message": f"Error durante el entrenamiento: {str(e)}"
            }), 500
        
        # Generar gráfica de recompensas
        try:
            agent.plot_training(episode_rewards)
            print("✓ Gráfica de recompensas generada")
        except Exception as e:
            print(f"✗ Error generando gráfica: {e}")
            return jsonify({
                "status": "error",
                "message": f"Error generando gráfica: {str(e)}"
            }), 500
        
        # Guardar modelo
        try:
            agent.save_model('static/modelo_entrenado.pkl')
            print("✓ Modelo guardado correctamente")
        except Exception as e:
            print(f"✗ Error guardando modelo: {e}")
        
        # CONVERTIR TIPOS NUMPY A PYTHON NATIVO PARA JSON
        final_reward = 0
        if episode_rewards:
            # Convertir numpy types a Python native types
            final_reward = float(episode_rewards[-1]) if hasattr(episode_rewards[-1], 'item') else int(episode_rewards[-1])
        
        return jsonify({
            "status": "success", 
            "message": f"Entrenamiento completado con {episodes} episodios",
            "episodes": int(episodes),
            "final_reward": final_reward
        })
        
    except Exception as e:
        print(f"✗ Error general en train_RL: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route("/test_RL", methods=["POST"])
def test_RL():
    """Endpoint para probar el modelo entrenado"""
    try:
        # Asegurar que la carpeta static existe
        os.makedirs('static', exist_ok=True)
        
        print("🧭 Iniciando prueba de política...")
        
        # Cargar modelo entrenado
        from RefuerzoPractico import GridWorldAgent
        agent = GridWorldAgent()
        
        if os.path.exists('static/modelo_entrenado.pkl'):
            print("✓ Cargando modelo entrenado existente")
            agent.load_model('static/modelo_entrenado.pkl')
        else:
            print("⚠️  No hay modelo entrenado, entrenando uno rápido...")
            # Si no hay modelo entrenado, entrenar uno rápido
            agent.train(episodes=100)
            agent.save_model('static/modelo_entrenado.pkl')
        
        # Generar trayectoria y gráfica
        best_path, actions = agent.get_best_path()
        print(f"✓ Trayectoria generada: {len(best_path)} pasos")
        
        # Guardar gráfica de trayectoria
        agent.plot_trajectory(best_path)
        print("✓ Gráfica de trayectoria guardada")
        
        # CONVERTIR TIPOS NUMPY A PYTHON NATIVO
        path_length = int(len(best_path))
        # Convertir tuplas de numpy a listas de Python
        path_python = [list(map(int, coord)) for coord in best_path]
        
        return jsonify({
            "status": "success",
            "message": "Simulación completada",
            "path_length": path_length,
            "path": path_python,
            "actions": actions
        })
        
    except Exception as e:
        print(f"✗ Error en test_RL: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Error en la simulación: {str(e)}"
        }), 500

# SOLUCIÓN SIMPLE: Saltar la creación si ya existen los archivos
def check_static_files():
    """Verificar que los archivos necesarios existan"""
    import os
    
    # Asegurar que static existe
    os.makedirs('static', exist_ok=True)
    
    # Lista de archivos necesarios
    needed_files = [
        'placeholder-rewards.png',
        'placeholder-trajectory.png'
    ]
    
    missing_files = []
    for file in needed_files:
        path = os.path.join('static', file)
        if not os.path.exists(path):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Archivos faltantes en static: {missing_files}")
        print("ℹ️  Puedes crearlos manualmente o el sistema los creará cuando sea necesario")
    else:
        print("✓ Todos los archivos static están presentes")

# En lugar de create_placeholder_images(), usa:
check_static_files()

if __name__ == "__main__":
    app.run(debug=True)