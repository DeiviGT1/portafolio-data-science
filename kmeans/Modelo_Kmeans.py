import warnings
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from sklearn import preprocessing 

warnings.filterwarnings("ignore")

class Clustering():

    # === Funcion para ordenar datos
    def __init__(self, dataframe_despacho, dataframe_ventas):
        self.dataframe = dataframe_despacho.copy()
        self.dataframe = self.dataframe.merge(dataframe_ventas, on='item')
        self.dataframe["rotacion"] = self.dataframe["venta"]/self.dataframe["unidades_despachadas"]
        self.dataframe["rotacion"]=np.where((self.dataframe["rotacion"]>=1),1,self.dataframe["rotacion"])
        self.dataframe["venta"]=np.where((self.dataframe["venta"]>=self.dataframe["unidades_despachadas"]),self.dataframe["unidades_despachadas"],self.dataframe["venta"])
        self.dataframe["genero_categoria"] = self.dataframe["genero"]+"_"+self.dataframe["categoria"]
        self.dataframe["genero_categoria"] = self.dataframe["genero_categoria"].str.replace(" ","_")
        self.dataframe["recuento"] = self.dataframe.groupby("genero_categoria")["genero_categoria"].transform("count")
        self.dataframe = self.dataframe[self.dataframe["recuento"] >= 5]
        self.dataframe = self.dataframe.drop(["recuento"], axis=1)
        self.dataframe["genero_categoria"] = np.where((self.dataframe["unidades_despachadas"] > 900)&(self.dataframe["genero_categoria"] == "HOMBRE_CAMISETA"), "HOMBRE_CAMISETA_LOTE_GRANDE",
                                    np.where((self.dataframe["unidades_despachadas"] > 600)&(self.dataframe["genero_categoria"] == "HOMBRE_TANK"), "HOMOBRE_TANK_LOTE_GRANDE",
                                    np.where((self.dataframe["unidades_despachadas"] <= 600)&(self.dataframe["genero_categoria"] == "HOMBRE_TANK"), "HOMBRE_TANK_LOTE_MEDIO",
                                    np.where((self.dataframe["unidades_despachadas"] <= 900)&(self.dataframe["genero_categoria"] == "HOMBRE_CAMISETA"),"HOMBRE_CAMISETA_LOTE_MEDIO",
                                    self.dataframe["genero_categoria"]))))
        
        self.df_final = pd.DataFrame()
        ruta = 
        self.df_azares = pd.read_csv(ruta, index_col=0)
        

        # === Se crea el df_items ya que en el analisis no e tiene en cuenta este dato
        # === pero si se unen al final por medio del indice que se mantiene
        self.df_items = self.dataframe.copy()
        self.df_items = self.df_items[['item', 'genero', 'categoria', 'unidades_despachadas']]
    
    # === Funcion para medir distancias
    def asignacion_datos(self, datos, centros):
        lista_mejores_normas = []
        self.datos = datos
        self.centros = centros
        for dato in self.datos:
            normas_por_dato = []
            # === Primero tenemos que convertir los arrays en dimension 
            # === (1,2) para que funcione la formula de norma
            for centroide in self.centros:
                dato = np.array(dato).reshape(1, len(centroide))
                centroide = np.array(centroide).reshape(1, len(centroide))
                norma = cdist(dato, centroide, 'euclidean')
                # === En una lista comenzamos a acumular las distancias 
                normas_por_dato.append(norma)
            # === Para cada uno de los datos elegimos la norma minima 
            # === y obtenemos el indice del cual está mas cercano
            lista_mejores_normas.append(normas_por_dato.index(min(normas_por_dato)))        

        arr_normas = np.array(lista_mejores_normas)

        # === Une al array principal la lista de las mejores normas
        return np.c_[datos, arr_normas]

    # === Función para actualizar centroides
    def definir_centroides(self, clusters):
        lst_x=[]
        lst_y=[]
        lista_centroides=[]
        self.clusters = clusters
        self.dataframe["genero_categoria"] = np.where((self.dataframe["unidades_despachadas"] > 900)&(self.dataframe["genero_categoria"] == "HOMBRE_CAMISETA"), "HOMBRE_CAMISETA_LOTE_GRANDE",
                                    np.where((self.dataframe["unidades_despachadas"] > 600)&(self.dataframe["genero_categoria"] == "HOMBRE_TANK"), "HOMOBRE_TANK_LOTE_GRANDE",
                                    np.where((self.dataframe["unidades_despachadas"] <= 600)&(self.dataframe["genero_categoria"] == "HOMBRE_TANK"), "HOMBRE_TANK_LOTE_MEDIO",
                                    np.where((self.dataframe["unidades_despachadas"] <= 900)&(self.dataframe["genero_categoria"] == "HOMBRE_CAMISETA"),"HOMBRE_CAMISETA_LOTE_MEDIO",
                                    self.dataframe["genero_categoria"]))))
        try:
            for genero_categoria in self.dataframe["genero_categoria"].unique():
                # === Creamos un df para almacerar los genero_categoria
                df_centroides = self.dataframe.loc[self.dataframe["genero_categoria"] == genero_categoria][['venta','rotacion']]
                # === Transformamos los datos para estandarizarlos
                dic_scalers = {genero_categoria: preprocessing.StandardScaler().fit_transform(df_centroides)}
                # === Creamos el modelo k_means que tendra el numero de clusters elegidos
                dic_kmeans = {genero_categoria: KMeans(n_clusters = self.clusters).fit(dic_scalers[genero_categoria])}
                dic_centroides = {genero_categoria: dic_kmeans[genero_categoria].cluster_centers_}
                for i in range(self.clusters):
                    lista_centroides.append([genero_categoria])
                # === Por ultimo, con los centroides creamos los subdividimos hasta obtener 
                # === cada coordenada  para cada centroide para cada categoria
                for conjunto in dic_centroides.values():
                    for coordenada in conjunto:
                        i = 0
                        for elemento in coordenada:
                            if i == 0:
                                lst_x.append(elemento)
                            else: lst_y.append(elemento)
                            i+=1
        except: print(f'La categoria {genero_categoria} no tiene suficientes datos para obtener sus centroides')
        # === Luego se organiza el dataframe para obtener el formato correcto
        lst = [lista_centroides]+[lst_x]+[lst_y]
        centroides = pd.DataFrame(lst).T
        centroides.columns =["genero_categoria", "eje_x", "eje_y"]
        centroides["genero_categoria"] = centroides["genero_categoria"].astype("str")
        centroides["genero_categoria"] = centroides["genero_categoria"].str.replace("'","")
        centroides["genero_categoria"] = centroides["genero_categoria"].str.replace("'","")
        centroides["genero_categoria"] = centroides["genero_categoria"].str.replace("[","")
        centroides["genero_categoria"] = centroides["genero_categoria"].str.replace("]","")
        centroides = centroides[["eje_x", "eje_y", "genero_categoria"]]

        return centroides

    # === Funcion principal para ejecutar el kMeans
    def funcion_principal(self, df_items_despacho):
        self.df_items_despacho = df_items_despacho
        for genero_categoria in self.dataframe["genero_categoria"].unique():
            df_copia = self.dataframe.copy()
            df_copia = df_copia.loc[df_copia["genero_categoria"] == genero_categoria][['venta','rotacion']]
            dic_scalers = {genero_categoria: preprocessing.StandardScaler().fit_transform(df_copia)}
            dic_centroides = {genero_categoria: self.df_azares[self.df_azares["genero_categoria"] == genero_categoria][["eje_x", "eje_y"]]}
            np_centroide = dic_centroides[genero_categoria].to_numpy()
            try:
                dic_asignacion = {genero_categoria: self.asignacion_datos(dic_scalers[genero_categoria], np_centroide)}
                df_copia["coordenada_x_1"] = dic_asignacion[genero_categoria][:,0]
                df_copia["coordenada_y_1"] = dic_asignacion[genero_categoria][:,1]
                df_copia["identificador"] = dic_asignacion[genero_categoria][:,2]
                df_copia["color"] = np.where((df_copia["identificador"]==0),"blue",np.where((df_copia["identificador"]==1),"green",np.where((df_copia["identificador"]==2),"orange","red")))
                df_copia["medida"] = df_copia["venta"] * df_copia["rotacion"]
                df_colores = df_copia.groupby("color").mean()
                df_colores = df_colores[["medida"]]
                df_colores = df_colores.sort_values(by="medida", ascending=False)
                try:
                    df_colores["calificacion"] = ["AAA+", "AAA", "A", "B"]
                except:
                    df_colores["calificacion"] = ["Revisar"]*len(df_colores["calificacion"])
                df_copia = df_copia.merge(df_colores, right_index=True, left_on="color")
                df_copia = df_copia[["venta", "rotacion", "calificacion"]]
                self.df_final = pd.concat([self.df_final, df_copia])
            except: 
                print(f'{genero_categoria} No tiene centroides definidos')

        self.df_final = self.df_final.merge(self.df_items, right_index=True, left_index=True)
        self.df_final = self.df_final.merge(self.df_items_despacho, right_on = 'item', left_on = 'item')
        self.df_final = self.df_final.sort_values(by=['genero', 'categoria', 'calificacion'])
        return self.df_final
