import os
import numpy as nump
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

'''
=====================================================
1. Configuración corporativa y de setup
=====================================================
'''

def estiloCorporativo():
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.left'] = True
    plt.rcParams['axes.spines.bottom'] = True
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['grid.color'] = '#eeeeee'
    plt.rcParams['figure.figsize'] = (10, 6)

def setDirectorioExportacion(path='exportaciones_bi'):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

'''
=====================================================
2. Funciones de gráficas gerenciales
=====================================================
'''

def plotLinealidad(ruta_salida):
    """Gráfica 1: Demuestra que el consumo no es predecible linealmente (R² bajo)"""
    nump.random.seed(42)
    x_cantidad_procesos = nump.random.uniform(1, 1000, 200)
    y_porcentaje_cpu = 10 + nump.log(x_cantidad_procesos) * 2 + nump.random.normal(0, 15, 200)
    
    plt.figure()
    axes = sns.regplot(x = x_cantidad_procesos, y = y_porcentaje_cpu, 
                        scatter_kws={'alpha':0.4, 'color': '#2c3e50'},
                        line_kws={'color': '#e74c3c', 'label': 'Tendencia Lineal (R² = 0.187)'})
    plt.title('Linealidad y Relación entre Volumen de Cantidad de Procesos y Porcentaje de CPU', fontweight='bold', pad=20)
    plt.xlabel('Cantidad de Procesos Concurrentes', labelpad=10)
    plt.ylabel('Porcentaje de CPU', labelpad=10)
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, '01_linealidad_cantidad_procesos_cpu.png'), dpi=300)
    plt.close()

def plotRadarAmenazas(ruta_salida):
    """Gráfica 2: K-Means segmentando el estado del servidor"""
    # Simulamos los resultados de tu Silhouette Score de 0.9410
    n = 300
    df_kmeans = pd.DataFrame({
        'CPU': nump.concatenate([nump.random.normal(10, 5, n), nump.random.normal(85, 10, n), nump.random.normal(20, 5, n)]),
        'RAM': nump.concatenate([nump.random.normal(15, 5, n), nump.random.normal(20, 5, n), nump.random.normal(90, 8, n)]),
        'Cluster': ['Operación Normal (Reposo)']*n + ['Anomalía CPU (Posible Ataque)']*n + ['Fuga de Memoria (Crítico)']*n
    })
    
    # Paleta semáforo corporativa
    colores = {"Operación Normal (Reposo)": "#2ecc71", 
               "Anomalía CPU (Posible Ataque)": "#f39c12", 
               "Fuga de Memoria (Crítico)": "#c0392b"}
    
    plt.figure()
    sns.scatterplot(data=df_kmeans, x='CPU', y='RAM', hue='Cluster', palette=colores, alpha=0.7, s=60)
    
    plt.title("Segmentación Automática de Recursos (K-Means)", fontweight='bold', pad=20)
    plt.xlabel("Uso de CPU (%)")
    plt.ylabel("Uso de Memoria RAM (%)")
    plt.axvline(80, color='gray', linestyle='--', alpha=0.5) # Línea de advertencia
    plt.axhline(80, color='gray', linestyle='--', alpha=0.5) # Línea de advertencia
    plt.legend(title="Estado del Sistema", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, '02_radar_amenazas.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    
'''
=====================================================
3. Ejecución final del pipeline de exportación
=====================================================
'''

def plotRelojArenaForecasting(ruta_salida):
    """Gráfica 3: Series de tiempo previniendo la saturación (Fechas corregidas)"""
    # Empezamos el historial el 9 de abril de 2026 para que el corte histórico (día 45) caiga exactamente a finales de mayo de 2026.
    dias = pd.date_range(start='2026-04-09', periods=60)
    
    # 45 días de historia real (Abril -> Finales de Mayo)
    consumo_historico = nump.linspace(40, 75, 45) + nump.random.normal(0, 3, 45)
    
    # 15 días de predicción hacia el futuro (Finales de Mayo -> Junio)
    ultimo_valor_historico = consumo_historico[-1]
    prediccion = nump.linspace(ultimo_valor_historico, 95, 16)
    
    limite_inferior = prediccion - 5
    limite_superior = prediccion + 5
    
    plt.figure(figsize=(12, 6))
    
    # Datos históricos
    plt.plot(dias[:45], consumo_historico, color='#2980b9', label='Consumo Histórico', linewidth=2)
    # Proyección
    plt.plot(dias[44:], prediccion, color='#e67e22', linestyle='--', label='Predicción (Forecasting)', linewidth=2)
    # Cono de incertidumbre
    plt.fill_between(dias[44:], limite_inferior, limite_superior, color='#e67e22', alpha=0.2, label='Margen de Error')
    
    # Línea fatal de saturación
    plt.axhline(y=90, color='#c0392b', linestyle='-.', linewidth=2, label='Límite Crítico (90% - Riesgo de Caída)')
    
    # Resaltar el punto de cruce
    fecha_caida = dias[44 + nump.argmax(prediccion >= 90)]
    plt.scatter([fecha_caida], [90], color='red', s=100, zorder=5)
    
    # Formatear la fecha para que se vea bonita en el texto
    fecha_texto = fecha_caida.strftime('%d de %b')
    plt.annotate(f'Punto de Quiebre\n({fecha_texto})', 
                 xy=(fecha_caida, 90), 
                 xytext=(fecha_caida - pd.Timedelta(days=12), 95),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 fontweight='bold')
    
    plt.title("Proyección de Saturación de RAM a 15 Días", fontweight='bold', pad=20)
    plt.ylabel("Consumo de RAM (GB o %)")
    plt.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, '03_forecasting_saturacion.png'), dpi=300)
    plt.close()
    
def plotTopRiesgos(ruta_salida):
    """Gráfica 4: Análisis de texto traducido a impacto de negocio"""
    # Resultados del Text Analysis de journalctl
    errores = ['OOM-Killer (Out of Memory)', 'Timeout en Conexión DB', 'Segfault (Violación Segmento)', 
               'Falla de Autenticación SSH', 'Deadlock en Hilos']
    frecuencias = [1240, 850, 420, 310, 150]
    
    df_errores = pd.DataFrame({'Error Crítico': errores, 'Frecuencia en Logs': frecuencias})
    
    plt.figure()
    ax = sns.barplot(x='Frecuencia en Logs', y='Error Crítico', data=df_errores, palette='Reds_r')
    
    # Añadir las etiquetas de datos al final de cada barra para lectura rápida
    for i in ax.containers:
        ax.bar_label(i, padding=5, fontweight='bold', color='#555555')
        
    plt.title("Top 5 Amenazas Silenciosas en Infraestructura", fontweight='bold', pad=20)
    plt.xlabel("Apariciones en el último mes (journalctl)")
    plt.ylabel("") # Ocultamos el label del eje Y porque los nombres ya explican qué es
    
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, '04_top_riesgos_texto.png'), dpi=300)
    plt.close()

if __name__ == "__main__":
    estiloCorporativo()
    ruta_exportacion = setDirectorioExportacion()
    
    print(f"Exportando visualizaciones corporativas al directorio: {ruta_exportacion}")
    plotLinealidad(ruta_exportacion)
    plotRadarAmenazas(ruta_exportacion)
    plotRelojArenaForecasting(ruta_exportacion)
    plotTopRiesgos(ruta_exportacion)