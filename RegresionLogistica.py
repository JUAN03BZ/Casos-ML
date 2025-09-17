import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import io, base64

# Cargar datos
df = pd.read_csv("Datos.csv")

# Variables independientes y dependiente
X = df[["Tiempo_Pagina", "Num_Clics", "Fuente_Trafico", "Nivel_Ingresos"]]
y = df["Compra"]

# Columnas categóricas
categorical_features = ["Fuente_Trafico", "Nivel_Ingresos"]

# Definimos preprocesador para columnas categóricas y escalado para numéricas
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), ["Tiempo_Pagina", "Num_Clics"])
    ]
)

# Construimos pipeline con preprocesador + clasificador
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, solver="lbfgs"))
])

# Separar datos y entrenar modelo una vez
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model.fit(X_train, y_train)

def predecir_compra(tiempo, clics, fuente, ingresos):
    # Crear dataframe de un solo registro con los datos del formulario
    nuevo = pd.DataFrame(
        [[tiempo, clics, fuente, ingresos]],
        columns=["Tiempo_Pagina", "Num_Clics", "Fuente_Trafico", "Nivel_Ingresos"]
    )
    # Obtener probabilidad de clase 1 (compra)
    prob = model.predict_proba(nuevo)[0][1] * 100

    if prob < 40:
        resultado = "No compra"
    elif prob < 70:
        resultado = "Posible compra"
    else:
        resultado = "Compra segura"

    return round(prob, 2), resultado

def obtener_matriz_confusion():
    # Predicciones sobre conjunto fijo de test
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Compra", "Compra"],
                yticklabels=["No Compra", "Compra"])
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.title("Matriz de Confusión")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf-8")
