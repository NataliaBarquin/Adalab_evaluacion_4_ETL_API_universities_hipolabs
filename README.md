# DA-promoE-Mod2-Evaluacion-sprint2-NataliaBarquin
Evaluación 2 del Módulo 2 de Natalia Barquín

Este repositorio incluye la Evaluación 2 del Módulo 2 del Bootcamp de Data Analytics.
Esta evaluación ha consistido en un proceso de ETL (Extracción, Transformación y Carga) de la API Universities Hipolabs (este es su [link](http://universities.hipolabs.com/search?country=NOMBREPAIS).
En este [repositorio](https://github.com/Hipo/university-domains-list) de GitHub pued encontrarse documentación sobre esta API.
Se han extraído datos de la API referentes a 3 países indicados, se han aplicado procesos de limpieza y transformación a los datos y posteriormente se han añadido a una base de datos en MySQL para realizar posteriores consultas.
Finalmente, se ha incluido el código generado dentro de una clase para optimizar el proceso.

#### DIRECTORIOS DEL REPOSITORIO

- **notebooks:** se incluyen dos archivos jupyter:
    - evaluacion_natalia_ejercicios : incluye la evaluación desglosada en los diferentes ejercicios.
    - evaluacion_natalia_clase : incluye el código generado durante la evaluación dentro de una clase.    
- **data:** se incluye un archivo generado y guardado en el proceso de transformación.

#### LENGUAJES UTILIZADOS
Python.
SQL.

#### LIBRERÍAS UTILIZADAS
- **Requests** para hacer llamadas a API's. Documentación en este [link](https://pypi.org/project/requests/).
- **Numpy:** para análisis de datos. Documentación en este [link](https://numpy.org/).
- **Pandas:** para análisis de datos. Documentación en este [link](https://pandas.pydata.org/).
- **Sidetable** para exploración de datos. Documentación en este [link](https://pypi.org/project/sidetable/).
- **Geopy** Para acceder a datos geográficos. Documentación en este [link](https://geopy.readthedocs.io/en/stable/).
- **Mysql.connector** Para conectarse con MySQL. Documentación en este [link](https://pypi.org/project/mysql-connector-python/).
- **Os** Para acceder a archivo .env donde se guarda oculta la contraseña. Documentación en este [link](https://docs.python.org/es/3.10/library/os.html).
