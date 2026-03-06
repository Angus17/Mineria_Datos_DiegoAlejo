# Práctica 3: Visualización y Análisis Gráfico de Logs de Sistema

Esta práctica culmina el flujo de minería de datos al generar visualizaciones a partir del dataset limpio de logs de `journalctl`. Se producen gráficas estadísticas que permiten identificar patrones de uso, distribuciones de recursos, anomalías (outliers) y relaciones entre variables del sistema Linux.

## 📋 Tabla de Contenidos

- [Objetivo](#-objetivo)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Metodología y Flujo de Trabajo](#-metodología-y-flujo-de-trabajo)
  - [1. Diagramas de Pie](#1-diagramas-de-pie)
  - [2. Histogramas](#2-histogramas)
  - [3. Boxplots (Diagramas de Caja)](#3-boxplots-diagramas-de-caja)
  - [4. Bar Plots (Gráficas de Barras)](#4-bar-plots-gráficas-de-barras)
  - [5. Scatter Plots (Diagramas de Dispersión)](#5-scatter-plots-diagramas-de-dispersión)
- [Gráficas Generadas](#-gráficas-generadas)
- [Instrucciones de Ejecución](#-instrucciones-de-ejecución)
- [Análisis Detallado de Resultados](#-análisis-detallado-de-resultados)
- [Conclusiones del Análisis Visual](#-conclusiones-del-análisis-visual)

## 🎯 Objetivo

Generar un conjunto de visualizaciones estadísticas a partir del dataset limpio (Práctica 1), con el fin de explorar gráficamente la distribución de recursos (CPU, RAM), la longitud de los mensajes de log, la proporción de severidades y la actividad por usuario y tipo de proceso en un sistema Ubuntu corriendo en una ThinkPad E490.

## 📂 Estructura del Proyecto

La carpeta `Practica_3/` contiene:

```text
Practica_3/
├── Graficas/
│   ├── pie_User.png                          # Pie: Top 5 proporciones por Usuario.
│   ├── pie_TipoProceso.png                   # Pie: Top 5 proporciones por Tipo de Proceso.
│   ├── pie_Nivel_Severidad.png               # Pie: Top 5 proporciones por Nivel de Severidad.
│   ├── histograma_Uso_CPU.png                # Histograma: Distribución de Uso de CPU.
│   ├── histograma_Uso_RAM.png                # Histograma: Distribución de Uso de RAM.
│   ├── histograma_LongitudMensaje.png        # Histograma: Distribución de Longitud de Mensaje.
│   ├── boxplot_Uso_CPU.png                   # Boxplot: Detección de outliers en CPU.
│   ├── boxplot_Uso_RAM.png                   # Boxplot: Detección de outliers en RAM.
│   ├── boxplot_LongitudMensaje.png           # Boxplot: Detección de outliers en Longitud de Mensaje.
│   ├── barplot_User.png                      # Barras: Top 10 usuarios por cantidad de logs.
│   ├── barplot_TipoProceso.png               # Barras: Top 10 tipos de proceso por cantidad de logs.
│   ├── barplot_Nivel_Severidad.png           # Barras: Top 10 niveles de severidad por cantidad de logs.
│   ├── scatter_Uso_CPU_vs_Uso_RAM.png        # Dispersión: Relación CPU vs RAM.
│   └── scatter_LongitudMensaje_vs_Uso_CPU.png # Dispersión: Relación Longitud de Mensaje vs CPU.
├── scripts/
│   └── graficas_journalctl.py                # Script principal de generación de gráficas.
└── README.md                                 # Documentación de la práctica.
```

## 🛠 Requisitos Previos

- **Python 3.x**
- Librerías: `pip install pandas seaborn matplotlib`
- El archivo CSV limpio generado en la Práctica 1 (`dataset_linux_journalctl_limpio.csv`).
- Variables de entorno configuradas:
  - `DATASET`: Ruta absoluta al archivo CSV limpio.
  - `GRAFICAS`: Ruta al directorio donde se guardarán las gráficas.

## 🚀 Metodología y Flujo de Trabajo

El script `graficas_journalctl.py` genera **14 gráficas** organizadas en 5 tipos de visualización, separando las columnas del dataset en dos grupos:

- **Columnas numéricas:** `Uso_CPU`, `Uso_RAM`, `LongitudMensaje`
- **Columnas categóricas:** `User`, `TipoProceso`, `Nivel_Severidad`

Se utiliza **Seaborn** como librería principal de visualización (sobre Matplotlib) con el tema `whitegrid` y paleta `muted` para mantener una estética limpia y profesional.

---

### 1. Diagramas de Pie

Muestran la **proporción relativa** de las 5 categorías más frecuentes en cada variable categórica.

| Gráfica | Descripción |
| --------- | --------- |
| `pie_User.png` | Proporción de logs generados por los 5 usuarios más activos. |
| `pie_TipoProceso.png` | Distribución porcentual de los tipos de proceso (Kernel, Daemon, Aplicación, etc.). |
| `pie_Nivel_Severidad.png` | Proporción de logs por nivel de severidad (INFO, WARNING, ERROR). |

**¿Para qué sirve?** Permite visualizar de un vistazo qué categorías dominan el dataset. Por ejemplo, qué porcentaje de logs son de `root` vs. `angus20`.

---

### 2. Histogramas

Muestran la **distribución de frecuencia** de las variables numéricas con 50 bins y una curva de densidad (KDE) superpuesta.

| Gráfica | Descripción |
|---------|-------------|
| `histograma_Uso_CPU.png` | Distribución del consumo de CPU de los procesos. |
| `histograma_Uso_RAM.png` | Distribución del consumo de RAM de los procesos. |
| `histograma_LongitudMensaje.png` | Distribución de la longitud (en caracteres) de los mensajes de log. |

**¿Para qué sirve?** Revela si los datos están sesgados, tienen distribución normal o presentan concentraciones inusuales. Es común ver que la mayoría de procesos consumen 0% de CPU/RAM, con pocos picos altos.

---

### 3. Boxplots (Diagramas de Caja)

Detectan **outliers** y muestran la dispersión estadística (mediana, cuartiles, rango intercuartílico) de cada variable numérica.

| Gráfica                        | Descripción                                                     |
| -------------------------------|-----------------------------------------------------------------|
| `boxplot_Uso_CPU.png`          | Identifica procesos con consumo de CPU anormalmente alto.       |
| `boxplot_Uso_RAM.png`          | Identifica procesos con consumo de RAM anormalmente alto.       |
| `boxplot_LongitudMensaje.png`  | Identifica mensajes de log inusualmente largos o cortos.        |

**¿Para qué sirve?** Los puntos fuera de los "bigotes" son **anomalías** potenciales. En un sistema Linux real, esto puede revelar procesos problemáticos o fugas de memoria.

---

### 4. Bar Plots (Gráficas de Barras)

Muestran el **Top 10** de categorías con mayor cantidad de registros en el dataset.

| Gráfica | Descripción |
|---------|-------------|
| `barplot_User.png` | Los 10 usuarios que más logs generan en el sistema. |
| `barplot_TipoProceso.png` | Los 10 tipos de proceso más frecuentes. |
| `barplot_Nivel_Severidad.png` | Conteo de logs por nivel de severidad. |

**¿Para qué sirve?** Identifica rápidamente los actores principales del sistema. Es esperable que `root` y `angus20` dominen, y que `INFO` sea la severidad más común.

---

### 5. Scatter Plots (Diagramas de Dispersión)

Exploran la **correlación** entre pares de variables numéricas, coloreados por `Nivel_Severidad` para añadir una dimensión analítica.

| Gráfica                                      | Variables                  | Descripción                                                       |
|----------------------------------------------|----------------------------|-------------------------------------------------------------------|
| `scatter_Uso_CPU_vs_Uso_RAM.png`             | CPU vs RAM                 | ¿Los procesos que consumen más CPU también consumen más RAM?      |
| `scatter_LongitudMensaje_vs_Uso_CPU.png`     | Longitud de Mensaje vs CPU | ¿Los procesos con mayor carga generan mensajes más largos?        |

**¿Para qué sirve?** Permite descubrir relaciones ocultas entre variables. Si los puntos de ERROR (rojo) se concentran en zonas de alto consumo, podría indicar una correlación entre fallos y sobrecarga.

---

## 📊 Gráficas Generadas

En total se generan **14 gráficas** distribuidas de la siguiente manera:

| Tipo de Gráfica | Cantidad | Archivos |
| --------------- | -------- | -------- |
| Diagramas de Pie | 3 | `pie_User.png`, `pie_TipoProceso.png`, `pie_Nivel_Severidad.png` |
| Histogramas | 3 | `histograma_Uso_CPU.png`, `histograma_Uso_RAM.png`, `histograma_LongitudMensaje.png` |
| Boxplots | 3 | `boxplot_Uso_CPU.png`, `boxplot_Uso_RAM.png`, `boxplot_LongitudMensaje.png` |
| Bar Plots | 3 | `barplot_User.png`, `barplot_TipoProceso.png`, `barplot_Nivel_Severidad.png` |
| Scatter Plots | 2 | `scatter_Uso_CPU_vs_Uso_RAM.png`, `scatter_LongitudMensaje_vs_Uso_CPU.png` |

## 💻 Instrucciones de Ejecución

1. **Configurar variables de entorno**:
   Define las rutas necesarias antes de ejecutar el script:

   ```bash
   export DATASET="/ruta/a/Practica_1/csv/dataset_linux_journalctl_limpio.csv"
   export GRAFICAS="/ruta/a/Practica_3/Graficas"
   ```

2. **Ejecutar el script de gráficas**:

   ```bash
   python scripts/graficas_journalctl.py
   ```

3. **Verificar resultados**:
   Las 14 gráficas se guardarán automáticamente en la carpeta `Graficas/`. El script imprime la ruta de cada gráfica conforme se genera.

## 📈 Análisis Detallado de Resultados

A continuación, se presenta la interpretación técnica de las visualizaciones generadas, fundamentales para entender el comportamiento del sistema operativo.

### 1. Distribución de Frecuencias (Histogramas)

Los histogramas permiten observar la forma en que se distribuyen los datos numéricos.

- **Histograma de Uso de CPU:** Muestra una **Asimetría Positiva (Right-Skewed)** extrema. La mayoría de los procesos consumen cerca del 0%, lo que indica un sistema eficiente en reposo.
- **Histograma de Uso de RAM:** Similar al CPU, la concentración de datos en valores bajos confirma que el registro de logs no impacta significativamente la memoria del equipo.
- **Histograma de Longitud de Mensaje:** Identifica que la mayoría de los eventos generan mensajes cortos, típicos de estados informativos de servicios en segundo plano.

### 2. Detección de Anomalías (Boxplots)

Los diagramas de caja son vitales para identificar valores que se salen de la norma general del sistema.

- **Boxplot de CPU:** Se observan múltiples *outliers* que superan el 100%. Estos representan picos de actividad de aplicaciones multihilo (como el entorno de desarrollo u otras herramientas de usuario).
- **Boxplot de RAM:** Los puntos por encima del "bigote" superior indican procesos que, aunque estadísticamente atípicos, llegan a consumir hasta un 2.5% de la memoria disponible durante eventos específicos.
- **Boxplot de Longitud de Mensaje:** El diagrama revela una distribución altamente asimétrica en la verbosidad del sistema. La caja principal comprimida cerca del cero indica que la inmensa mayoría de los logs son mensajes muy cortos y concisos. La densa línea de puntos superiores muestran eventos esporádicos pero sumamente extensos (alcanzando hasta ~2,500 caracteres). Estos picos corresponden a registros detallados como *stack traces* de errores, alertas complejas o volcados de memoria de ciertas aplicaciones.

### 3. Proporciones y Categorías (Pie Charts)

Se utilizaron líneas de enlace para una lectura clara de las proporciones.

- **Proporción por Usuario:** El usuario `root` domina con el 58.7% de los logs, reflejando la actividad constante de los demonios del kernel de Linux.
- **Nivel de Severidad:** El 93% de los registros son de nivel `INFO`, lo que indica un sistema altamente estable con pocos errores críticos interrumpiendo el flujo.
- **Tipo de Proceso:** La proporción muestra que en su mayoría son logs orientados al Kernel del sistema Linux.

### 4. Gráficas de Barras (Top 10)

Permiten comparar rápidamente el volumen de actividad entre diferentes actores del sistema.

- **Bar Plot de Procesos:** Identifica a los servicios de sistema y el kernel como los principales emisores de ruido dentro de `journalctl`.
- **Bar Plot de Severidad:** Cuantifica visualmente la desproporción masiva entre mensajes puramente informativos frente a las advertencias y fallos reales.
- **Bar Plot de Usuarios:** Identifica la cantidad de Logs generado por los primeros 10 usuarios del sistema Ubuntu, como resultado final, `root` es el usuario que genera más logs.

### 5. Análisis de Correlación (Scatter Plots)

Exploran si existe una relación de dependencia directa entre variables clave del rendimiento.

- **CPU vs RAM:** No existe una correlación lineal fuerte ($R \approx 0$). Esto significa que un proceso puede ser intensivo en cómputo sin agotar la memoria, y viceversa, confirmando que ambas métricas aportan valor independiente para el modelado.
- **Longitud de Mensaje vs CPU:** Se observa que los errores ocurren de manera transversal, independientemente de la carga actual del procesador.

## 📌 Conclusiones del Análisis Visual

- **Dominancia de `root` y `angus20`:** La mayoría de los logs del sistema son generados por estos dos usuarios, lo cual es esperable en un sistema Ubuntu de escritorio con un solo usuario activo.
- **Distribución sesgada de recursos:** La gran mayoría de procesos registran 0% de CPU y RAM; solo unos pocos procesos (como `gnome-shell`, `code`, `userdir`) presentan consumos significativos, visibles como outliers en los boxplots.
- **Predominancia de `INFO`:** La severidad más común es `INFO`, con una proporción menor de `WARNING` y `ERROR`, lo que indica un sistema generalmente estable.
- **Procesos del Kernel dominan:** El tipo de proceso más frecuente es `Sistema (Kernel)`, seguido de `Usuario (Aplicación)`, consistente con la naturaleza del `journalctl`.
- **Correlaciones débiles:** Los scatter plots muestran que no hay una correlación lineal fuerte entre CPU y RAM, ni entre longitud de mensaje y CPU, lo cual sugiere que cada variable aporta información independiente al análisis.

El sistema opera en un estado de reposo altamente eficiente, donde los picos de consumo son causados por aplicaciones de usuario y no por el sistema operativo base.

**La Evidencia:** Cerca del 93% de los logs corresponden a la severidad 'INFO', y el usuario root genera el 58.7% de la actividad en segundo plano. Los diagramas de dispersión demostraron que no existe correlación lineal (R ≈ 0) entre el consumo de CPU y RAM.

---
**Curso:** Minería de Datos\
**Autor:** Diego Leonardo Alejo Cantú\
**Matrícula:** 2013810
