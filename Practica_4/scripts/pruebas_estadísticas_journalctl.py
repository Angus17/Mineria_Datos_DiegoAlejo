import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# ==========================================
# 0. CONFIGURACIÓN Y CARGA
# ==========================================
# Leer el archivo CSV
ruta_csv = os.getenv("DATASET", "../Practica_1/csv/dataset_linux_journalctl_limpio.csv")
try:
    df_dataset = pd.read_csv(ruta_csv)
except FileNotFoundError:
    print("Error: Dataset no encontrado.")
    exit()

print("=== PRÁCTICA 4: PRUEBAS ESTADÍSTICAS ===")
print("Variable Independiente (Etiqueta): Nivel_Severidad")
print("Variable Dependiente (Continua): Uso_CPU\n")

# Extraer los grupos basados en la variable independiente
grupos = df_dataset.groupby('Nivel_Severidad')['Uso_CPU'].apply(list)


# ==========================================
# 1. PRUEBA DE NORMALIDAD (Kolmogorov-Smirnov)
# ==========================================
print("--- 1. Prueba de Normalidad (Kolmogorov-Smirnov) ---")
print("Hipótesis Nula (H0): Los datos provienen de una distribución normal.")

todos_normales = True # Bandera para saber si todos pasaron

for severidad, uso_cpu in grupos.items():
    stat, p_value = stats.kstest(uso_cpu, 'norm')
    print(f"[{severidad}] -> Estadístico KS: {stat:.4f}, p-valor: {p_value:.4e}")
    if p_value < 0.05:
        todos_normales = False

# ==========================================
# ÁRBOL DE DECISIÓN ESTADÍSTICO
# ==========================================
if not todos_normales:
    print("\nConclusión KS: Al menos un grupo tiene p-valor < 0.05. Se rechaza H0.")
    print("Los datos NO siguen una distribución normal (Asimetría Positiva).")
    print("Justificación: La prueba ANOVA no es válida. Procedemos con Kruskal-Wallis.\n")
    
    # Ejecutamos la alternativa no paramétrica (Kruskal)
    print("--- 2. Prueba Ómnibus (Kruskal-Wallis) ---")
    kw_stat, p_value_kw = stats.kruskal(*grupos.values)
    print(f"Estadístico H: {kw_stat:.4f}, p-valor: {p_value_kw:.4e}")
    
    if p_value_kw < 0.05:
        print("\nConclusión Final: Se rechaza H0. Existen diferencias significativas en el uso de CPU entre severidades.")
    else:
        print("\nConclusión Final: No se rechaza H0. El nivel de severidad no afecta el consumo de CPU.")

else:
    print("\nConclusión KS: No se rechaza H0. Todos los grupos son normales.")
    print("Procedemos a revisar Homogeneidad de Varianzas.\n")
    
    # ==== 2. Homogeneidad de Varianzas (Levene) ====
    print("--- 2. Prueba de Homogeneidad de Varianzas (Levene) ---")
    stat_levene, p_value_levene = stats.levene(*grupos.values)
    print(f"Estadístico Levene: {stat_levene:.4f}, p-valor: {p_value_levene:.4e}")
    
    if p_value_levene < 0.05:
        print("\nConclusión Levene: Se rechaza H0. Las varianzas NO son homogéneas.")
        print("Justificación: ANOVA no es válida. Procedemos con Kruskal-Wallis.\n")
        
        # Ejecutamos Kruskal
        kw_stat, p_value_kw = stats.kruskal(*grupos.values)
        print(f"Estadístico H: {kw_stat:.4f}, p-valor: {p_value_kw:.4e}")
        if p_value_kw < 0.05:
            print("\nConclusión Final: Existen diferencias significativas en el uso de CPU entre severidades.")
        else:
            print("\nConclusión Final: No hay diferencias significativas.")
            
    else:
        print("\nConclusión Levene: No se rechaza H0. Las varianzas son homogéneas.")
        print("Los datos son perfectos. Procedemos con ANOVA clásica.\n")
        
        # ==== 3. Prueba ANOVA ====
        print("--- 3. Prueba ANOVA ---")
        stat_anova, p_value_anova = stats.f_oneway(*grupos.values)
        print(f"Estadístico ANOVA: {stat_anova:.4f}, p-valor: {p_value_anova:.4e}")
        
        if p_value_anova < 0.05:
            print("\nConclusión Final: Se rechaza H0. Existen diferencias significativas en el uso de CPU.")
        else:
            print("\nConclusión Final: No se rechaza H0. No existen diferencias significativas en el uso de CPU.")

# Generar gráfica de respaldo para el reporte
plt.figure(figsize=(10,6))
sns.boxplot(x='Nivel_Severidad', y='Uso_CPU', data=df_dataset, palette='Set2')
plt.title('Comparativa Estadística: Uso_CPU por Nivel_Severidad')
plt.ylim(-0.1, df_dataset['Uso_CPU'].quantile(0.99)) # Recortar outliers extremos
plt.savefig(os.getenv("GRAFICA_ESTADISTICA") + "/grafica_estadistica-UsoCPU-Nivel_Severidad.png")
print("\n[+] Gráfica guardada como 'grafica_estadistica-UsoCPU-Nivel_Severidad.png'.")