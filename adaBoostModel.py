import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import io
import base64

RANDOM_STATE = 42

def load_data():
    
    df = pd.read_csv("satisfaccion_cliente.csv")

    return df

df = load_data()
X = df.drop(columns=['Satisfaccion'])
y = df['Satisfaccion']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

cat_features = ['Tono agente', 'Canal contacto']
num_features = ['Tiempo atencion', 'Resolucion problema']

# Las opciones de las variables categóricas
tono_agente_opciones = ['Descortés', 'Neutral', 'Amable']
canal_contacto_opciones = ['Teléfono', 'Correo', 'Chat']



numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')), 
    ('scaler', StandardScaler()) 
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),  
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  
])


preprocessor = ColumnTransformer([
    ('num', numeric_transformer, num_features),
    ('cat', categorical_transformer, cat_features)
])


base_estimator = DecisionTreeClassifier(max_depth=1, random_state=RANDOM_STATE)
ada = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=RANDOM_STATE)

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', ada)
])


model.fit(X_train, y_train)

def evaluate():
    y_pred = model.predict(X_test)
    acc = round(accuracy_score(y_test, y_pred), 4)
    report = classification_report(y_test, y_pred, output_dict=True)
    matrix = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=["No satisfecho", "Satisfecho"])
    disp.plot(ax=ax, cmap=plt.cm.Blues)
    plt.title("Matriz de Confusión")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return {
        "accuracy": acc,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "confusion_matrix_img": img_base64
    }

def predict_label(features, threshold=0.5):
    df_features = pd.DataFrame([features])
    proba = model.predict_proba(df_features)[0, 1]
    label = "Sí" if proba >= threshold else "No"
    return label, round(proba, 4)
