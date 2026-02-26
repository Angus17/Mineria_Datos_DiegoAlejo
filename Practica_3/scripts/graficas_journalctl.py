from os import getenv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Cargamos el dataset limpio
dataset = pd.read_csv(getenv('DATASET'))

# Configuramos el estilo de las gráficas
sns.set_theme(style="whitegrid", palette="muted")

# Separamos las columnas por tipo para facilitar los bucles
columnas_numericas = ['Uso_CPU', 'Uso_RAM', 'LongitudMensaje']
columnas_categoricas = ['User', 'TipoProceso', 'Nivel_Severidad']