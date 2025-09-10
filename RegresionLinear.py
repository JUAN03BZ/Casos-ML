import pandas as pd
from sklearn.linear_model import LinearRegression
import locale

# Configurar locale para formato colombiano
try:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")  # Linux / Mac
except:
    try:
        locale.setlocale(locale.LC_ALL, "Spanish_Colombia")  # Windows
    except:
        # Si falla, usar locale por defecto
        pass

# Dataset sencillo: años de experiencia + nivel educativo
# Nivel educativo: 1 = Secundaria, 2 = Técnico, 3 = Universitario, 4 = Posgrado
data = {
    "Experiencia": [1, 2, 3, 5, 7, 10, 12, 15],
    "Educacion": [1, 2, 2, 3, 3, 4, 4, 4],
    "Sueldo": [1800000, 1500000, 2000000, 2400000, 3500000, 5000000, 6000000, 7500000]
}

df = pd.DataFrame(data)

X = df[["Experiencia", "Educacion"]]
y = df["Sueldo"]

# Entrenar modelo
model = LinearRegression()
model.fit(X, y)

# Salario mínimo 2025 (aprox.)
SALARIO_MINIMO = 1300000  

def predict_salary(experiencia, educacion):
    """Predice el salario y lo devuelve en formato de pesos colombianos"""
    result = model.predict([[experiencia, educacion]])[0]

    # Evitar valores negativos o absurdos -> piso en salario mínimo
    if result < SALARIO_MINIMO:
        result = SALARIO_MINIMO

    try:
        # Formato colombiano con puntos de miles
        return locale.format_string("%d COP", int(result), grouping=True)
    except:
        # Fallback si falla locale -> usa comas
        return f"${result:,.0f} COP"
