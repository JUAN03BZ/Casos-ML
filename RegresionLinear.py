import pandas as pd
from sklearn.linear_model import LinearRegression
import locale


try:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8") 
except:
    try:
        locale.setlocale(locale.LC_ALL, "Spanish_Colombia") 
    except:
        pass

# años de experiencia + nivel educativo = Sueldo
data = {
    "Experiencia": [1, 1, 2,2,3,3,4,4,6,6,8,8,10,10,12,12,14,14,15,15],
    "Educacion":   [1, 7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7],
    "Sueldo": [1400000, 7000000,1600000,7300000,1700000,7500000,1800000,7700000 ,2000000,8000000,2200000
               ,8300000,2300000,8600000,2400000,9000000,2500000,9800000,2700000,10000000],
}

df = pd.DataFrame(data)

X = df[["Experiencia", "Educacion"]]
y = df["Sueldo"]

model = LinearRegression()
model.fit(X, y)


SALARIO_MINIMO = 1400000  

def predict_salary(experiencia, educacion):
    """Predice el salario y lo devuelve en formato de pesos colombianos"""
    result = model.predict([[experiencia, educacion]])[0]

    if result < SALARIO_MINIMO:
        result = SALARIO_MINIMO

    try:
        return locale.format_string("%d COP", int(result), grouping=True)
    except:
        return f"${result:,.0f} COP"
    
