# Mineria_Datos_DiegoAlejo

**Repositorio para la materia de Minería de Datos**

Este repositorio cuenta con dos ramas importantes:

`main # Producción`
`dev # Development`

## Estructura de ramas

*main*: Es la rama principal donde se encuentra el entregable final para la materia. Todos los cambios que residan aquí se consideran
definitivos, estables y listos para ser calificados.
*dev*: Es la rama de desarrollo. Aquí es donde se realiza la programación activa y se suben los avances frecuentes de los scripts y el análisis de datos. Una vez el código ha sido probado y los resultados son correctos,
se realiza un **Merge**  hacia la rama `main`.

Una vez que los scripts y el análisis de datos en la rama `dev` funcionan correctamente, se
integran a la rama principal. El proceso técnico para realizar la "mezcla" es el siguiente:

```
# Primero asegurarnos de estar en la rama principal
git checkout main

# Fusionar los cambios de desarrollo con la rama principal
git merge dev

# Por último, subir los cambios finales al servidor
git push origin main

```

*Diego Leonardo Alejo Cantú*
*Estudiante de Licenciatura en Ciencias Computacionales*

Última fecha de actualización: **10/02/2026 12:50 a.m**
