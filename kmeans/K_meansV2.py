from Modelo_Kmeans_v2 import Clustering
import sys

### ============================== ACTIVAR PARA CORRER EL MODELO ============================== ###
ruta =
sys.path.insert(0, ruta)
from SQL_consultas import df_despacho, df_ventas, df_items_despacho

clustering = Clustering(df_despacho, df_ventas)
calificacion = clustering.funcion_principal(df_items_despacho)
ruta_export = 
calificacion.to_csv(f'{ruta_export}\calificacion.csv')



### ============================== ACTIVAR PARA ACTUALIZAR CENTROIDES ============================== ###
sys.path.insert(0, ruta)
from SQL_consultas_centroides import (df_despacho_centroides,
                                        df_ventas_centroides)
numeros_de_clusters = int(input("Ingrese el numero de clusters a usar: "))
clustering = Clustering(df_despacho_centroides, df_ventas_centroides)
centroides = clustering.definir_centroides(numeros_de_clusters)
ruta_export =
centroides.to_csv(f'{ruta_export}\centroides.csv')
