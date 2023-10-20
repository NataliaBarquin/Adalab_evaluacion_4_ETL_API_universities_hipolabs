import requests
import pandas as pd
import numpy as np
import sidetable
from geopy.geocoders import Nominatim
import mysql.connector

import os
from dotenv import load_dotenv
load_dotenv()

import src.soporte as sp
import src.soporte_variables as sp_var


api = sp.Extraccion_limpieza(sp_var.lista_paises, 'US_Can_Arg')

df_universidades = api.extraer_df_api()

api.homogeneizar_columnas(df_universidades)

df_universidades['name'] = api.limpiar_comillas(df_universidades, 'name')

df_universidades_exp = api.aplicar_explode(df_universidades)

df_universidades_exp[df_universidades_exp['name'] == 'Cégep de Saint-Jérôme']

api.eliminar_duplicados(df_universidades_exp)

df_universidades_exp.stb.missing()

df_universidades_exp['state_province'] = (df_universidades_exp['state_province'].apply(sp.convertir_a_nan))

api.imputar_nulos(df_universidades_exp, 'state_province')

df_universidades_exp["state_province"] = df_universidades_exp['state_province'].apply(lambda estado: sp_var.dicc_estados.get(estado, estado))

lista_estados = df_universidades_exp['state_province'].unique().tolist()

df_geopy = api.sacar_latitud_longitud_geopy(lista_estados)

df_unido = api.mergear_dfs(df_universidades_exp, df_geopy, 'state_province')

carga = sp.Carga('localhost', 'Universidades')

carga.crear_bbdd()

carga.crear_tabla(sp_var.tabla_paises)

carga.crear_tabla(sp_var.tabla_universidades)


for indice, fila in df_unido.iterrows():

        latitud = fila['latitude']
        longitud = fila['longitude']

        if pd.isna(latitud):
                latitud = 'NULL'

        if pd.isna(longitud):
                longitud = 'NULL'

        id_estado = carga.sacar_id_estado(fila['state_province'],fila['country'])

        if type(id_estado) is not int:

                insertar_paises = f"""
                        INSERT INTO `Universidades`.`paises` (nombre_pais, nombre_provincia, latitud, longitud) 
                        VALUES ( "{fila['country']}", "{fila['state_province']}", {latitud}, {longitud});
                        """
                carga.insertar_datos(insertar_paises)
        else:
                pass
        

for indice, fila in df_unido.iterrows():

        id_estado = carga.sacar_id_estado(fila['state_province'], fila['country'])
        insertar_universidades = f"""
                INSERT INTO `Universidades`.`universidades` (nombre_universidad, pagina_web, paises_id_estado) 
                VALUES ( "{fila['name']}", "{fila['web_pages']}", {id_estado});
                """
        
        carga.insertar_datos(insertar_universidades)



