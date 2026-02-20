import pandas as pd
import os

# Cargar el dataset limpio
df = pd.read_csv(os.getenv('DATASET'))

# 1. Crear diccionarios de mapeo para simular el AUTO_INCREMENT
# Esto asignará un número único a cada texto (ej. {'root': 1, 'angus20': 2})
map_usuarios = {val: i+1 for i, val in enumerate(df['User'].unique())}
map_tipos = {val: i+1 for i, val in enumerate(df['TipoProceso'].unique())}
map_procesos = {val: i+1 for i, val in enumerate(df['NombreProceso'].unique())}
map_severidades = {val: i+1 for i, val in enumerate(df['Nivel_Severidad'].unique())}

# 2. Inserciones en los Catálogos (Dimensiones) forzando el ID
sql_usuarios = [f"INSERT INTO usuario (id_usuario, nombre) VALUES ({id_val}, '{nombre}');" 
                for nombre, id_val in map_usuarios.items()]


sql_tipos_proceso = [f"INSERT INTO tipo_proceso (id_tipo_proceso, tipo_de_proceso) VALUES ({id_val}, '{tipo}');" 
                     for tipo, id_val in map_tipos.items()]

sql_procesos = [f"INSERT INTO proceso (id_proceso, nombre_proceso) VALUES ({id_val}, '{proceso}');" 
                for proceso, id_val in map_procesos.items()]

sql_severidades = [f"INSERT INTO severidad (id_severidad, nivel_severidad) VALUES ({id_val}, '{sev}');" 
                   for sev, id_val in map_severidades.items()]

# 3. Generar las sentencias SQL para la Tabla de Hechos (logs_sistema)
sql_statements = []
for index, row in df.iterrows():
    # Buscar el ID correspondiente en nuestros diccionarios
    id_usr = map_usuarios[row['User']]
    id_proc = map_procesos[row['NombreProceso']]
    id_tipo = map_tipos[row['TipoProceso']]
    id_sev = map_severidades[row['Nivel_Severidad']]
    
    # Escapar comillas simples en el mensaje de log para que MySQL no arroje error de sintaxis
    mensaje_seguro = str(row['MensajeLog']).replace("'", "''")
    
    sql = (f"INSERT INTO logs_sistema (fecha_proceso, id_usuario, id_proceso, id_tipo_proceso, pid, "
           f"uso_cpu, uso_ram, estado_proceso, longitud_mensaje, mensaje_log, id_severidad, is_error) "
           f"VALUES ('{row['FechaProceso']}', {id_usr}, {id_proc}, {id_tipo}, {row['PID']}, "
           f"{row['Uso_CPU']}, {row['Uso_RAM']}, '{row['EstadoProceso']}', {row['LongitudMensaje']}, "
           f"'{mensaje_seguro}', {id_sev}, {row['Is_Error']});")
    
    sql_statements.append(sql)
    
# 4. Guardar todo en el archivo .sql
with open(os.getenv('SQL_INSERTS', 'inserciones_journalctl.sql'), 'w', encoding='utf-8') as f:
    f.write("-- INSERCIONES DE CATÁLOGOS\n")
    for sql in sql_usuarios: f.write(sql + '\n')
    for sql in sql_tipos_proceso: f.write(sql + '\n')
    for sql in sql_procesos: f.write(sql + '\n')
    for sql in sql_severidades: f.write(sql + '\n')
    
    f.write("\n-- INSERCIONES DE LOGS\n")
    for sql in sql_statements: f.write(sql + '\n')

print("¡Archivo SQL generado con éxito y relaciones mapeadas!")