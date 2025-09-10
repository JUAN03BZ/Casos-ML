import pandas as pd
from sklearn.linear_model import LinearRegression

# Dataset sencillo: años de experiencia + nivel educativo
# Nivel educativo: 1 = Secundaria, 2 = Técnico, 3 = Universitario, 4 = Posgrado
data = {
    "Experiencia": [1, 2, 3, 5, 7, 10, 12, 15],
    "Educacion": [1, 2, 2, 3, 3, 4, 4, 4],
    "Sueldo": [1200, 1500, 2000, 2800, 3500, 5000, 6000, 7500]
}

df = pd.DataFrame(data)

X = df[["Experiencia", "Educacion"]]
y = df["Sueldo"]

model = LinearRegression()
model.fit(X, y)

def predict_salary(experiencia, educacion):
    result = model.predict([[experiencia, educacion]])[0]
    return round(result, 2)
