import requests
import pandas as pd
import numpy as np
import sidetable
from geopy.geocoders import Nominatim
import mysql.connector

import os




class Extraccion_limpieza:

    def __init__(self, lista_paises, nombre_fichero_coord):

        self.lista_paises = lista_paises
        self.nombre_fichero_coord = nombre_fichero_coord

    def extraer_df_api(self):

        """Crea una lista con los 3 países que queremos estudiar y realiza la llamada a la API y extracción de datos de la misma para cada uno de los países.
        Después crea un dataframe con los datos de cada país y los unifica en un único dataframe.
        Args:
            No recibe.
        Returns:
            df: dataframe unido con los datos de los 3 países.
        """

        df_unido = pd.DataFrame()

        for pais in self.lista_paises:

            url = f'http://universities.hipolabs.com/search?country={pais}'

            response = requests.get(url=url)

            response.status_code

            response.reason
            
            df = pd.json_normalize(response.json())

            df_unido = pd.concat([df_unido, df], ignore_index = True)
        
        return df_unido
    

    def homogeneizar_columnas(self, df, col = 'domains'):

        """Reemplaza los guiones de los nombres de las columnas del dataframe por barra baja, y
            elimina columnas redundantes.
        Args:
            df: dataframe original.
            col: columna redundante, parámetro por defecto.
        Returns:
            df: dataframe modificado.
        """
        
        df.rename(columns = {col: col.replace('-', '_') for col in df.columns}, inplace = True)
        df.drop(col, axis = 1, inplace = True)

        return df
    
    def limpiar_comillas(self, df, col):

        """Elimina las comillas de los registros de la columna que se le indique.
        Args:
            df: dataframe original.
            col: columna sobre la que queremos eliminar las comillas.
        Returns:
            df: dataframe con la columna sin comillas.
        """

        return df[col].str.replace('"', '').str.replace("'", "")


    def aplicar_explode(self, df, col = 'web_pages'):

        """Aplica método explode a columnas con más de un valor por registro.
        Args:
            df: dataframe original.
            col: col a aplicar explode, parámetro por defecto.
        Returns:
            df: dataframe modificado.
        """
        
        return df.explode(col, ignore_index= True)
    

    def eliminar_duplicados(self, df, col = 'name'):

        """Elimina las filas duplicadas en base a una columna que le indiquemos.
        Args:
            df: dataframe.
            col: columna sobre la que buscar duplicados.
        Returns:
            df: dataframe sin las filas duplicadas.
        """

        if df.duplicated([col]).sum() > 0:
            print(f'Tenemos {df.duplicated([col]).sum()} duplicados en la columna "{col}", los eliminaremos.')
            return df.drop_duplicates(subset = col, inplace = True, ignore_index = True)
        
        else:
            print(f'No tenemos duplicados en la columna {col}.')

# preguntar
    def convertir_a_nan(self, valor):

        """convierte los valores None a np.nan.
        Args:
            valor (str): valor None
        Returns:
            valor (np.nan): valor np.nan
        """

        if valor == None:
            return np.nan
        else:
            return valor


    def imputar_nulos(self, df, col):

        """convierte los valores nulos al valor de string 'Unknow'.
        Args:
            df (df): dataframe.
            col (col): columna sobre la que queremos imputar los valores nulos.
        Returns:
            df: dataframe con nulos imputados.
        """

        return df[col].replace(np.nan, 'Unknow', inplace = True)


    def sacar_latitud_longitud_geopy(self, lista):

        """Usando la librería Geopy, obtiene la latitud y la longitud de una lista de provincias que
        le indiquemos, con ello crea un dataframe con las columnas provincia, latitud y longitud.
        Si la provincia es desconocida, devuelve un valor nulo para latitud y longitud.
        Args:
            lista (list): lista con localizaciones.
        Returns:
            df (df): dataframe de 3 columnas (provincia, latitud y longitud).
        """

        lista_latitud = []
        lista_longitud = []

        for estado in lista:

            if estado != 'Unknow':
                geo = Nominatim(user_agent = 'Natalia')
                localizacion = geo.geocode(estado)
                lista_latitud.append(localizacion.latitude)
                lista_longitud.append(localizacion.longitude)
        
            else:
                lista_latitud.append(np.nan)
                lista_longitud.append(np.nan)

        diccionario = {
            'state_province' : lista,
            'latitude' : lista_latitud,
            'longitude' : lista_longitud
            }

        df = pd.DataFrame(diccionario)
        df.to_csv(f'data/coordenadas_{self.nombre_fichero_coord}.csv') 

        return df


    def abrir_latitud_longitud_fichero(self):

        """Abre el archivo guardado en el anterior método. Este método está pensado para poder trabajar con unos datos
        extraídos previamente de la librería geopy en caso de que en el momento actual la librería no funcione bien.
        Args:
            No recibe.
        Returns:
            df (df): dataframe de 3 columnas guardado.
        """       
    
        return pd.read_csv(f'../data/coordenadas_{self.nombre_fichero_coord}.csv', index_col = 0)


    def mergear_dfs(self, df1, df2, col):

        """Mergea los 2 dataframes creados con esta clase.
        Args:
            df1 (df): primer dataframe a unir.
            df2 (df): segundo dataframe a unir.
            col (df): columna por la que queremos unir los dataframes.
        Returns:
            df (df): dataframe unido.
        """
    
        return df1.merge(df2, on = col)
    


def convertir_a_nan(valor):
    """convierte los valores None a np.nan.

    Args:
        valor (str): valor None

    Returns:
        valor (np.nan): valor np.nan
    """

    if valor == None:
        return np.nan
    else:
        return valor
    


class Carga:
    
    def __init__(self, host, bbdd):

        self.host = host
        self.bbdd = bbdd


    def crear_bbdd(self):

        """Usando mysql.connector, crea en MySQL una base de datos.
        Args:
            nombre de la base de datos (str): el nombre que queremos poner a nuestra base de datos.
        Returns:
            No tiene. Crea directamente la base de datos en MySQL.
        """
        
        conexion = mysql.connector.connect(
                        host = self.host,
                        user= os.getenv('user'),
                        password= os.getenv('password'))
        
        mycursor = conexion.cursor()

        try:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.bbdd};")
            conexion.commit() 

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)


    def crear_tabla(self, query):

        """Usando mysql.connector, crea en MySQL una tabla en una base de datos.
        Args:
            nombre de la base de datos (str): la base de datos donde queremos crear nuestra tabla.
            consulta (str): la consulta con la que creamos la tabla.
        Returns:
            No tiene. Crea directamente la tabla en MySQL.
        """

        conexion = mysql.connector.connect(
                                host = self.host,
                                user= os.getenv('user'),
                                password= os.getenv('password'), 
                                database=f"{self.bbdd}")
        
        mycursor = conexion.cursor()
        
        try: 
            mycursor.execute(query)
        
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)


    def insertar_datos(self, query):
    
        """Usando mysql.connector, inserta datos en una tabla de una base de datos.
        Args:
            nombre de la base de datos (str): la base de datos donde queremos insertar los datos.
            consulta (str): la consulta con la que insertamos los datos.
        Returns:
            No tiene. Inserta los datos directamente en la tabla en MySQL.
        """

        conexion = mysql.connector.connect(
                                host = self.host,
                                user= os.getenv('user'),
                                password= os.getenv('password'), 
                                database=f"{self.bbdd}")
        
        mycursor = conexion.cursor()
        
        try: 
            mycursor.execute(query)
            conexion.commit() 

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)


    def sacar_id_estado(self, estado, pais):

        """Usando mysql.connector, selecciona el id de un estado de nuestra base de datos.
        Args:
            nombre de la base de datos (str): la base de datos de la que queremos extraer la información.
            estado (str): estado del que queremos sacar el id.
            pais (str): país al que pertenece el estado del que queremos sacar el id.
        Returns:
            id (str): el id del estado.
        """
        conexion = mysql.connector.connect(
                                host = self.host,
                                user= os.getenv('user'),
                                password= os.getenv('password'), 
                                database=f"{self.bbdd}")
        
        mycursor = conexion.cursor()

        query_sacar_id = f"SELECT id_estado FROM paises WHERE nombre_provincia = '{estado}' AND nombre_pais = '{pais}'"
        
        # puede que el id de la ciudad que estamos intentando insertar no este en nuestra BBDD, de modo que usaremos un try except para evitar errores
        try: 
            mycursor.execute(query_sacar_id)
            id_est = mycursor.fetchall()[0][0]
            
            return id_est
        
        except: 
            return "Lo siento, no tenemos ese estado en la BBDD y por lo tanto no te podemos dar su id. "
        
    
    def cerrar_conexion(self):

        """Cierra la conexión con MySQL."""

        self.conexion.close()
