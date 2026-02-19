# La clave para limpiar un dataset es entenderlo bien.
# Eliminar duplicados
# Eliminar filas con valores faltantes
# Eliminar filas con ruido en el log
# Transformar datos para que sean más fáciles de analizar (por ejemplo, convertir fechas a un formato estándar)

import pandas as pd

# Cargamos el dataset

df_crudo = pd.read_csv('/home/angus20/Escritorio/Mineria_Datos_DiegoAlejo/Practica_1/csv/dataset_linux_journalctl.csv')

print("Filas del dataset crudo:", len(df_crudo))

# Eliminamos filas duplicadas
df_limpio = df_crudo.drop_duplicates()

# Eliminamos filas con valores faltantes
df_limpio = df_limpio.dropna()

# Creamos una nueva columna "TipoProceso" basada en el contenido de "NombreProceso"
df_limpio['TipoProceso'] = "Aplicación"  # Valor por defecto

# Si el NombreProceso contiene caracteres de sistema (por ejemplo, corchetes []), lo clasificamos como "Sistema"
mask_sistema = df_limpio['NombreProceso'].str.contains(r'[\[\]]', na=False)
df_limpio.loc[mask_sistema, 'TipoProceso'] = 'Sistema (Kernel)'

# Si el NombreProceso termina en d o contiene "daemon", y es del usuario root, lo clasificamos como "Sistema (Daemon)"
mask_daemon = (df_limpio['NombreProceso'].str.endswith('d', na=False) | df_limpio['NombreProceso'].str.contains('daemon', case=False, na=False)) & (df_limpio['User'] != 'angus20')
df_limpio.loc[mask_daemon, 'TipoProceso'] = 'Sistema (Daemon)'

# Si el NombreProceso contiene algun caracteristico que lo haga un daemon pero el usuario es angus20, lo clasificamos como "Usuario (Daemon)"
mask_usuario_daemon = (df_limpio['NombreProceso'].str.endswith('d', na=False) | df_limpio['NombreProceso'].str.contains('daemon', case=False, na=False)) & (df_limpio['User'] == 'angus20')
df_limpio.loc[mask_usuario_daemon, 'TipoProceso'] = 'Usuario (Daemon)'

# Si el proceso lo esta ejecutando angus20 o cualquier usuario que no sea root o un daemon del sistema, lo clasificamos como "Usuario"
mask_usuario = (df_limpio['User'] != 'root') & ~mask_daemon & ~mask_sistema & ~mask_usuario_daemon
df_limpio.loc[mask_usuario, 'TipoProceso'] = 'Usuario (Aplicación)'

# Corregimos el formato de la columna 'FechaProceso' a un formato de fecha y hora estándar (DateTime)
df_limpio['FechaProceso'] = pd.to_datetime(df_limpio['FechaProceso'], errors='coerce', utc=True)

# Eliminamos ruido de la columna 'MensajeLog' y de 'NombreProceso' (por ejemplo, eliminando caracteres especiales, sobre todo los [] y :)
df_limpio['MensajeLog'] = df_limpio['MensajeLog'].str.replace(r'[^a-zA-Z0-9\s\.\-\/]', '', regex=True)
df_limpio['NombreProceso'] = df_limpio['NombreProceso'].str.replace(r'[\[\]:]', '', regex=True).str.strip().str.lower()

# Estandarizamos el texto a minusculas para evitar problemas de mayúsculas y minúsculas
df_limpio['User'] = df_limpio['User'].str.lower()
df_limpio['NombreProceso'] = df_limpio['NombreProceso'].str.lower()

# Eliminar registros donde el NombreProceso haya quedado vacío después de la limpieza
df_limpio = df_limpio[df_limpio['NombreProceso'] != '']

print("Filas del dataset limpio:", len(df_limpio))

# Guardamos el dataset limpio en un nuevo archivo CSV
df_limpio.to_csv('/home/angus20/Escritorio/Mineria_Datos_DiegoAlejo/Practica_1/csv/dataset_linux_journalctl_limpio.csv', index=False)
print("Dataset limpio guardado en '/home/angus20/Escritorio/Mineria_Datos_DiegoAlejo/Practica_1/csv/dataset_linux_journalctl_limpio.csv'")
