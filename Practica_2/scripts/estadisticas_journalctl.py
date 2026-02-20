import pandas as pd
import os

# 1. Cargar el dataset limpio
df = pd.read_csv(os.getenv('DATASET'))

print("============ 1. ESTADÍSTICAS DESCRIPTIVAS GENERALES ============")

# Estadísticas para variables numéricas (CPU, Memoria, PID, Is_Error)
print("\n--- Estadísticas Numéricas ---")
stats_numericas = df.describe()
print(stats_numericas)

# Estadísticas para variables categóricas (Texto, Usuario, Status)
print("\n--- Estadísticas Categóricas ---")
stats_categoricas = df.describe(include=['object'])
print(stats_categoricas)


print("\n=============== 2. AGRUPACIÓN POR ENTIDADES (GROUP BY) ============")

# Agrupación 1: Entidad "USUARIO"
# ¿Qué usuario consume más recursos y genera más errores?
print("\n--- Estadísticas agrupadas por USUARIO ---")
stats_usuario = df.groupby('User').agg({
    'Uso_CPU': ['mean', 'max'],    # Promedio y pico máximo de CPU
    'Uso_RAM': ['mean', 'max'], # Promedio y pico máximo de RAM
    'Is_Error': 'sum',               # Total de errores por usuario
    'NombreProceso': 'count'          # Cuántos procesos corrió
}).sort_values(by=('Is_Error', 'sum'), ascending=False) # Ordenar por el que tiene más errores
print(stats_usuario.head(10))

# Agrupación 2: Entidad "PROCESO"
# ¿Cuáles son los procesos más problemáticos o pesados?
print("\n--- Estadísticas agrupadas por PROCESO ---")
stats_proceso = df.groupby('NombreProceso').agg({
    'Uso_CPU': 'mean',             # CPU promedio
    'Uso_RAM': 'mean',          # Memoria promedio
    'Is_Error': 'sum',               # Errores totales del proceso
}).sort_values(by='Uso_RAM', ascending=False) # Ordenar por los que más RAM consumen
print(stats_proceso.head(10))

# Agrupación 3: Por "SEVERIDAD"
# ¿Cómo se distribuyen los niveles de severidad en el consumo de RAM?
print("\n--- Estadísticas agrupadas por SEVERIDAD ---")
stats_severidad = df.groupby('Nivel_Severidad')['Uso_RAM'].describe()
print(stats_severidad)

# # Para una mejor visualización, pasamos las estadisticas a un Excel
# with pd.ExcelWriter(os.getenv('STATISTICS_EXCEL')) as writer:
#     stats_numericas.to_excel(writer, sheet_name='Estadísticas Numéricas')
#     stats_categoricas.to_excel(writer, sheet_name='Estadísticas Categóricas')
#     stats_usuario.to_excel(writer, sheet_name='Agrupado por Usuario')
#     stats_proceso.to_excel(writer, sheet_name='Agrupado por Proceso')
#     stats_severidad.to_excel(writer, sheet_name='Agrupado por Severidad')