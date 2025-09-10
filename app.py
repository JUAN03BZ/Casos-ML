from flask import Flask, request, render_template
import RegresionLinear
import matplotlib
matplotlib.use("Agg")  # 👈 Usar backend sin interfaz gráfica
import matplotlib.pyplot as plt
import io
import base64

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
        plt.close()  # 👈 Cerrar figura para evitar fugas de memoria

    return render_template("practico.html", result=result, grafico_url=grafico_url)


if __name__ == "__main__":
    app.run(debug=True)
