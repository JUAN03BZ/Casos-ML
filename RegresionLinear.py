import pandas as pd
from sklearn.linear_model import LinearRegression
import locale

# Configurar locale para formato colombiano
try:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8") 
except:
    try:
        locale.setlocale(locale.LC_ALL, "Spanish_Colombia") 
    except:
        pass

# Dataset sencillo: años de experiencia + nivel educativo
data = {
    "Experiencia": [1, 2, 3, 5, 7, 10, 12, 15],
    "Educacion": [1, 2, 3, 4, 5, 5, 6, 7],
    "Sueldo": [1800000, 1500000, 2000000, 2400000, 3500000, 5000000, 6000000, 7500000]
}

df = pd.DataFrame(data)

X = df[["Experiencia", "Educacion"]]
y = df["Sueldo"]

model = LinearRegression()
model.fit(X, y)

# Salario mínimo 2025 (aprox.)
SALARIO_MINIMO = 1600000  

def predict_salary(experiencia, educacion):
    """Predice el salario y lo devuelve en formato de pesos colombianos"""
    result = model.predict([[experiencia, educacion]])[0]

    if result < SALARIO_MINIMO:
        result = SALARIO_MINIMO

    try:
        return locale.format_string("%d COP", int(result), grouping=True)
    except:
        return f"${result:,.0f} COP"
