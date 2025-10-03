import pandas as pd 
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# === 1. Cargar datos ===
df = pd.read_csv("/home/samuel/Downloads/dataset_pacientes_sintetico_normalizados_closterisados.csv")

# === 2. Detectar variables con alta correlación con el cluster ===
threshold = 0.3   # puedes ajustar este valor
corr = df.corr()["cluster"].abs()
high_corr = corr[corr > threshold].index.tolist()

print("🔎 Variables eliminadas por alta correlación con cluster:", high_corr)

# === 3. Construir dataset sin fuga de información ===
X = df.drop(high_corr, axis=1)   # quitamos variables con fuga
y = df["cluster"]

# === 4. Dividir datos ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === 5. Entrenar modelo ===
model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=5,             # regularizamos un poco
    min_samples_split=10,
    random_state=42
)
model.fit(X_train, y_train)

# === 6. Evaluación ===
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

# === 7. Validación cruzada para mejor estimación ===
scores = cross_val_score(model, X, y, cv=5)
print("\nAccuracies en validación cruzada:", scores)
print("Promedio:", scores.mean())

# === 8. Guardar modelo ===
model_path = os.path.join(os.path.dirname(__file__), "model_sin_fuga.joblib")
joblib.dump(model, model_path)
print(f"✅ Modelo guardado en {model_path}")