# Práctica 1: Limpieza y Preprocesamiento de Logs de Sistema

Esta práctica se enfoca en la fase inicial de la minería de datos: la limpieza y preparación del dataset. Se procesa un archivo de logs crudos del sistema Linux (`journalctl`) para eliminar ruido, estandarizar formatos y enriquecer la información mediante la clasificación de procesos.

## 📋 Tabla de Contenidos

- [Objetivo](#-objetivo)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Metodología de Limpieza](#-metodología-de-limpieza)
  - [1. Carga y Depuración Inicial](#1-carga-y-depuración-inicial)
  - [2. Ingeniería de Características (Feature Engineering)](#2-ingeniería-de-características-feature-engineering)
  - [3. Transformación y Estandarización](#3-transformación-y-estandarización)
- [Instrucciones de Ejecución](#-instrucciones-de-ejecución)

## 🎯 Objetivo

Transformar un dataset crudo de logs de sistema (CSV) en un conjunto de datos limpio y estructurado, listo para ser analizado o cargado en una base de datos. Se busca mejorar la calidad de los datos eliminando inconsistencias y categorizando la información.

## 📂 Estructura del Proyecto

La carpeta `Practica_1/` contiene:

```text
Practica_1/
├── csv/
│   ├── dataset_linux_journalctl.csv        # Archivo original con datos crudos.
│   └── dataset_linux_journalctl_limpio.csv # Resultado final tras la limpieza.
├── limpiar_dataset.py                      # Script principal de procesamiento.
├── .entorno/                               # Entorno virtual de Python (opcional).
└── README.md                               # Documentación de la práctica.
```

## 🛠 Requisitos Previos

- **Python 3.x**
- Librería **Pandas**: `pip install pandas`

## 🚀 Metodología de Limpieza

El script `limpiar_dataset.py` ejecuta los siguientes pasos de forma secuencial:

### 1. Carga y Depuración Inicial

- Se carga el dataset crudo desde `csv/dataset_linux_journalctl.csv`.
- **Eliminación de Duplicados:** Se descartan filas idénticas para evitar redundancia.
- **Manejo de Valores Nulos:** Se eliminan filas con datos faltantes que podrían afectar el análisis.

### 2. Ingeniería de Características (Feature Engineering)

Se crea una nueva columna llamada **`TipoProceso`** para clasificar el origen del log basándose en el nombre del proceso y el usuario:

- **Sistema (Kernel):** Procesos con nombres entre corchetes (ej. `[kworker]`).
- **Sistema (Daemon):** Servicios de sistema (terminan en 'd' o contienen "daemon") ejecutados por usuarios distintos al principal.
- **Usuario (Daemon):** Servicios en segundo plano ejecutados por el usuario principal (`angus20`).
- **Usuario (Aplicación):** Resto de procesos de usuario.
- **Aplicación:** Valor por defecto.

### 3. Transformación y Estandarización

- **Fechas:** Conversión de la columna `FechaProceso` al formato estándar `DateTime` (UTC).
- **Limpieza de Texto:**
  - `MensajeLog`: Eliminación de caracteres especiales no alfanuméricos.
  - `NombreProceso`: Eliminación de corchetes `[]`, dos puntos `:` y espacios extra.
- **Normalización:** Conversión de columnas de texto (`User`, `NombreProceso`) a minúsculas.

## 💻 Instrucciones de Ejecución

1. **Preparar el entorno**:
   Asegúrate de tener instalado Python y Pandas. Si usas el entorno virtual incluido:

   ```bash
   source .entorno/bin/activate
   ```

2. **Ejecutar el script de limpieza**:
   Desde la carpeta raíz del proyecto o dentro de `Practica_1`:

   ```bash
   python limpiar_dataset.py
   ```

3. **Verificar resultados**:
   El script generará (o sobrescribirá) el archivo limpio en:
   `csv/dataset_linux_journalctl_limpio.csv`

---
**Curso:** Minería de Datos\
**Autor:** Diego Leonardo Alejo Cantú
