# Práctica 2: Modelado Relacional, Carga y Análisis de Logs de Linux

Esta práctica se centra en la evolución del manejo de datos obtenidos previamente (`journalctl`). El objetivo principal ha sido migrar de un archivo plano (CSV) a un modelo de base de datos relacional normalizado, automatizar la generación de scripts SQL y realizar un análisis estadístico descriptivo utilizando Python.

## 📋 Tabla de Contenidos
- [Objetivo](#-objetivo)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Metodología y Flujo de Trabajo](#-metodología-y-flujo-de-trabajo)
  - [1. Diseño del Modelo E-R](#1-diseño-del-modelo-e-r)
  - [2. Creación del Esquema SQL](#2-creación-del-esquema-sql)
  - [3. Automatización de Inserciones](#3-automatización-de-inserciones)
  - [4. Análisis Estadístico](#4-análisis-estadístico)
- [Instrucciones de Ejecución](#-instrucciones-de-ejecución)

## 🎯 Objetivo
Transformar un dataset de logs de sistema Linux (limpiado en la Práctica 1) en una estructura de Base de Datos Relacional (SQL) para optimizar consultas y relaciones, además de extraer estadísticas clave sobre el consumo de recursos por usuario y proceso.

## 📂 Estructura del Proyecto

La carpeta `Practica_2/` contiene los siguientes directorios y archivos:

```text
Practica_2/
├── JSON/
│   └── journalctl-erd.erd.json      # Archivo JSON con la definición del Diagrama Entidad-Relación.
├── scripts/
│   ├── automatizar_insercionesSQL.py # Script para generar el archivo .sql con INSERTs masivos.
│   └── estadisticas_journalctl.py    # Script para generar reportes estadísticos con Pandas.
├── SQL/
│   ├── schema_journalctl.sql         # DDL: Creación de base de datos, tablas y relaciones.
│   └── inserciones_journalctl.sql    # DML: Archivo generado automáticamente con los datos.
└── README.md                         # Documentación de la práctica.
```

## 🛠 Requisitos Previos
- **Python 3.x**
- Librerías **Pandas**, **Os** (ya viene incluido), **Openpyxl**: `pip install pandas openpyxl`
- Un gestor de base de datos SQL (MySQL o MariaDB recomendados) para importar los archivos `.sql`.
- El archivo CSV limpio generado en la Práctica 1.

## 🚀 Metodología y Flujo de Trabajo

### 1. Diseño del Modelo E-R
Se diseñó un modelo relacional normalizado para evitar la redundancia de datos (como nombres de usuarios o tipos de procesos repetidos).
- **Archivo:** `JSON/journalctl-erd.erd.json`
- **Entidades identificadas (Tablas Dimensión):** `usuario`, `tipo_proceso`, `proceso`, `severidad`.
- **Tabla de Hechos:** `logs_sistema` (contiene las métricas como CPU, RAM y las llaves foráneas).

### 2. Creación del Esquema SQL
Se escribió el script DDL para materializar el diseño en la base de datos `journalctl`.
- **Archivo:** `SQL/schema_journalctl.sql`
- Define claves primarias (`AUTO_INCREMENT`), claves foráneas (`FOREIGN KEY`) y restricciones de integridad.

### 3. Automatización de Inserciones
Se desarrolló un script en Python para no escribir los `INSERT` a mano.
- **Archivo:** `scripts/automatizar_insercionesSQL.py`
- **Lógica:**
  1. Lee el CSV limpio.
  2. Crea diccionarios en memoria para mapear valores únicos (ej: "root" -> ID 1) para las tablas dimensión.
  3. Genera los `INSERT` para las tablas dimensión (`usuario`, `proceso`, etc.).
  4. Itera sobre cada fila del CSV para generar los `INSERT` de la tabla principal `logs_sistema` usando los IDs mapeados.
  5. Exporta todo a `SQL/inserciones_journalctl.sql`.

### 4. Análisis Estadístico
Se implementó un script para obtener métricas descriptivas de los datos.
- **Archivo:** `scripts/estadisticas_journalctl.py`
- **Métricas calculadas:**
  - Estadísticas generales (media, desviación, máx/mín) de CPU y RAM.
  - Agrupación por **Usuario**: ¿Quién genera más errores o consume más recursos?
  - Agrupación por **Proceso**: ¿Cuáles son los procesos más problemáticos o pesados?
  - Distribución por **Severidad**.

## 💻 Instrucciones de Ejecución

1. **Configurar Rutas**: Asegúrate de que los scripts de Python apunten al archivo CSV correcto (dataset limpio de la Práctica 1).

2. **Generar SQL de Datos**:
   Ejecuta el script de automatización:
   ```bash
   python scripts/automatizar_insercionesSQL.py
   ```
   Esto creará el archivo `inserciones_journalctl.sql`.

3. **Ver Estadísticas**:
   Ejecuta el script de análisis:
   ```bash
   python scripts/estadisticas_journalctl.py
   ```

4. **Cargar en Base de Datos**:
   Si tienes un servidor MySQL activo, puedes cargar los archivos en este orden:
   1. Ejecutar `schema_journalctl.sql`.
   2. Ejecutar `inserciones_journalctl.sql`.

---
**Curso:** Minería de Datos\
**Autor:** Diego Leonardo Alejo Cantú
