import os
from sys import stderr
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def mostrar_grafica(x, y, y_prediccion):
    plt.scatter(x, y, color='blue', label='Datos Reales')
    plt.plot(x, y_prediccion, color='red', label='Línea de Regresión')
    plt.xlabel('Uso de RAM')
    plt.ylabel('Uso de CPU')
    plt.title('Regresión Lineal: Uso de RAM vs Uso de CPU')
    plt.legend()
    plt.show()

print("=== PRÁCTICA 5: MODELO LINEAL ===")

# Cargamos la ruta del dataset de journalctl 
dataset = os.getenv("DATASET", "../Practica_1/csv/dataset_linux_journalctl_limpio.csv")

# Del dataset, seleccionamos las columnas relevantes para el modelo lineal, en este caso
# "Uso_CPU" y "Uso_RAM" serán las variables a seleccionar

try:
    df = pd.read_csv(dataset)
except FileNotFoundError:
    print("Error: Dataset no encontrado.", file=stderr)
    exit()

x = df[["Uso_RAM"]].values  # Variable independiente (RAM)
y = df["Uso_CPU"].values     # Variable dependiente (CPU)

# Creamos el modelo de regresión lineal
modelo = LinearRegression()

# Entrenamos el modelo con los datos
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
modelo.fit(x_train, y_train)

# Realizamos predicciones con los datos de prueba
y_prediccion = modelo.predict(x_test)

# Por último, evaluamos el rendimiento del modelo utilizando métricas como el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
mse_final = mean_squared_error(y_test, y_prediccion)
r2_final = r2_score(y_test, y_prediccion)

print(f"Error Cuadrático Medio (MSE): {mse_final:.4f}")
print(f"Coeficiente de Determinación (R²): {r2_final:.4f}")

# Visualizamos los resultados con un gráfico de dispersión y la línea de regresión
mostrar_grafica(x_test, y_test, y_prediccion)
os.makedirs(os.getenv("GRAFICA_MODELO_LINEAL"), exist_ok=True)
plt.savefig(os.getenv("GRAFICA_MODELO_LINEAL") + "/regresion_lineal_journalctl.png")
plt.close()