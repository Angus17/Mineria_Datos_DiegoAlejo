from os import getenv, makedirs
from os.path import exists 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Primero validar que el dataset exista antes de intentar cargarlo, para evitar errores posteriores.
DATASET_PATH = getenv('DATASET')

if not exists(DATASET_PATH):
    print(f"Error: No se encontró el dataset en: {DATASET_PATH}")
    sys.exit(1)


def guardar_grafica(nombre_archivo):
    """Función auxiliar para guardar la gráfica en el directorio especificado."""
    ruta_completa = f"{getenv('GRAFICAS')}/{nombre_archivo}"
    plt.tight_layout()
    plt.savefig(ruta_completa)
    plt.close()  # CRÍTICO: cerramos la figura para liberar memoria
    print(f"Gráfica guardada en: {ruta_completa}")


# Cargamos el dataset limpio
dataset = pd.read_csv(getenv('DATASET'))

# Configuramos el estilo de las gráficas
sns.set_theme(style="whitegrid", palette="muted")

print("Comenzando a generar gráficas...\n\n")

# Separamos las columnas por tipo para facilitar los bucles
columnas_numericas = ['Uso_CPU', 'Uso_RAM', 'LongitudMensaje']
columnas_categoricas = ['User', 'TipoProceso', 'Nivel_Severidad']

# Opcional pero recomendado: Crear un diccionario para nombres más amigables en las gráficas
mapa_nombres = {
    'Uso_CPU': 'Uso de CPU',
    'Uso_RAM': 'Uso de RAM',
    'LongitudMensaje': 'Longitud del Mensaje',
    'User': 'Usuario',
    'TipoProceso': 'Tipo de Proceso',
    'Nivel_Severidad': 'Nivel de Severidad'
}

# Es importante generar un directorio para guardar las gráficas, por ejemplo "graficas", y luego guardar cada gráfica con un nombre descriptivo dentro de ese directorio.
makedirs(getenv('GRAFICAS'), exist_ok=True)

# +++===============================================================================+++
# 1. DIAGRAMAS DE PIE (Los giagramas de pie nos muestran roporciones de Categorías)
# +++===============================================================================+++

for columna in columnas_categoricas:
    plt.figure(figsize=(7, 7))
    
    data_pie = dataset[columna].value_counts().head(5)  # Tomamos solo las 5 categorías más frecuentes para evitar gráficos saturados
    
    plt.pie(data_pie.values, labels=data_pie.index, autopct='%1.1f%%', 
            startangle=140, colors=sns.color_palette("pastel"))
    plt.title(f'Top 5 Proporciones por {mapa_nombres[columna]}', fontsize=14, fontweight='bold')
    guardar_grafica(f'pie_{columna}.png')
    plt.show()

# +++=====================================================================+++
# 2. HISTOGRAMAS (Con el histograma veremos la distribución de los datos)
# +++=====================================================================+++
for columna in columnas_numericas:
    plt.figure(figsize=(8, 5))
    # Usamos bins=50 para ver más detalle y KDE para la curva de tendencia
    sns.histplot(dataset[columna], bins=50, kde=True, color='royalblue')
    plt.title(f'Histograma de Distribución: {mapa_nombres[columna]}', fontsize=14)
    plt.xlabel(mapa_nombres[columna])
    plt.ylabel('Frecuencia')
    guardar_grafica(f'histograma_{columna}.png')
    plt.show()

# +++==============================================================+++
# 3. BOXPLOTS (Esto con el fin de detección de Outliers/anomalías)
# +++==============================================================+++
for columna in columnas_numericas:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=dataset[columna], color='darkorange')
    plt.title(f'Boxplot (Diagrama de Caja): {mapa_nombres[columna]}', fontsize=14)
    plt.tight_layout()
    guardar_grafica(f'boxplot_{columna}.png')
    plt.show()

# +++==========================================+++
# 4. PLOTS (Bar Plots para conteos categóricos)
# +++==========================================+++
for columna in columnas_categoricas:
    plt.figure(figsize=(10, 5))

    # Gráfica de barras de las 10 categorías más frecuentes
    top_10 = dataset[columna].value_counts().head(10)
    sns.barplot(x=top_10.values, y=top_10.index, palette='viridis')
    plt.title(f'Top 10 Conteo de Logs por {mapa_nombres[columna]}', fontsize=14)
    plt.xlabel('Cantidad de Logs')
    plt.ylabel(mapa_nombres[columna])
    guardar_grafica(f'barplot_{columna}.png')
    plt.show()

# +++=======================================================+++
# 5. SCATTER PLOTS (Para relación entre variables numéricas)
# +++=======================================================+++

# Creamos pares de variables para comparar en un bucle
pares_scatter = [('Uso_CPU', 'Uso_RAM'), ('LongitudMensaje', 'Uso_CPU')]

for x_col, y_col in pares_scatter:
    plt.figure(figsize=(8, 6))
    
    # Verificamos que Nivel_Severidad exista para el hue, si no, lo omitimos
    hue_parametro = 'Nivel_Severidad' if 'Nivel_Severidad' in dataset.columns else None
    
    # Aqui lo coloreamos por 'Nivel_Severidad' para darle un toque analítico avanzado
    sns.scatterplot(data=dataset, x=x_col, y=y_col, hue=hue_parametro, alpha=0.6, palette='deep')
    plt.title(f'Relación: {mapa_nombres.get(x_col, x_col)} vs {mapa_nombres.get(y_col, y_col)}', fontsize=14)
    plt.xlabel(mapa_nombres.get(x_col, x_col))
    plt.ylabel(mapa_nombres.get(y_col, y_col))
    guardar_grafica(f'scatter_{x_col}_vs_{y_col}.png')
    plt.show()

print("¡Todas las gráficas generadas y guardadas exitosamente!")