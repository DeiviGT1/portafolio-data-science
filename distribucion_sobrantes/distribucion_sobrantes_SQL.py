import pandas as pd
import numpy as np
import xlsxwriter
from tqdm import tqdm
from consultas_sql import df_inventario, df_despacho, df_ventas, dis_sobrantes, fecha_sale, recogida_sale, distribucion_tiendas, CP, ruta_1, ruta_2, ruta_3

#========================================================================#
#  ======================== Lector de rutas ======================== #
#========================================================================#
df_dis_sobrantes=pd.read_excel(dis_sobrantes, index_col=False)
df_fecha_sale=pd.read_excel(fecha_sale, index_col=False)
df_recogida_sale=pd.read_excel(recogida_sale, index_col=False)
df_distribucion_tiendas=pd.read_excel(distribucion_tiendas, index_col=False)
df_CP=pd.read_excel(CP, index_col=False)

#========================================================================#
#  ======================== Organizar tablas ======================== #
#========================================================================#
def orden_tablas_excel(tabla_1):
    try: 
        tabla_1.set_index('Item', inplace=True)
        tabla_1.columns=[c.replace(" ", "_") for c in tabla_1.columns]
    except: 
        try:
            tabla_1.set_index('ITEM', inplace=True)
            tabla_1.columns = [c.replace(" ", "_") for c in tabla_1.columns]
        except:
            tabla_1.columns=[c.replace(" ", "_") for c in tabla_1.columns]
            tabla_1 = tabla_1[tabla_1["TIPO"]=="P"] #<-  Filtro
            tabla_1["CORTO"] = tabla_1["CORTO"].str.upper()


    return tabla_1

def orden_tablas_sql(tabla_1):
    
    tabla_1["Items"] = tabla_1["item"]
    tabla_1.set_index('Items', inplace=True)
    
    return tabla_1

def merge_tablas(tabla_1, tabla_2):
    tabla_1 = tabla_1
    tabla_2 = tabla_2

    tabla_1=tabla_1.assign(Validador=tabla_1.index.isin(tabla_2.index))
    tabla_1=tabla_1[tabla_1["Validador"]==True] #<- Filtro
    tabla_1=tabla_1.groupby(["item", "tienda"]).sum().iloc[:,[0]]
    tabla_1.reset_index(inplace = True, level='tienda')
    tabla_1["index"]=tabla_1.index

    return tabla_1

df_despacho = orden_tablas_sql(df_despacho)
df_ventas = orden_tablas_sql(df_ventas)
df_inventario = orden_tablas_sql(df_inventario)
df_dis_sobrantes = orden_tablas_excel(df_dis_sobrantes)
df_fecha_sale = orden_tablas_excel(df_fecha_sale)
df_recogida_sale = orden_tablas_excel(df_recogida_sale)
df_distribucion_tiendas = orden_tablas_excel(df_distribucion_tiendas)
df_CP = orden_tablas_excel(df_CP)
df_ventas = merge_tablas(df_ventas, df_dis_sobrantes)
df_despacho = merge_tablas(df_despacho, df_dis_sobrantes)
df_inventario = merge_tablas(df_inventario, df_dis_sobrantes)
df_inventario = df_inventario[df_inventario["inventario"]>=2]

df_dis_sobrantes=df_dis_sobrantes.assign(Prueba_sale_1=df_dis_sobrantes.index.isin(df_recogida_sale.index)) # <- Buscar si un valor está en otro DF
df_dis_sobrantes=df_dis_sobrantes.assign(Prueba_sale_2=df_dis_sobrantes.index.isin(df_fecha_sale.index))
df_dis_sobrantes=df_dis_sobrantes.assign(Prueba_sale_3=df_dis_sobrantes.index.isin(df_CP.index))
df_inventario=df_inventario.merge(df_ventas, how="left", right_on=["index","tienda"], left_on=["index","tienda"]).set_axis(df_inventario.index)
df_inventario=df_inventario.merge(df_despacho, how="left", right_on=["index","tienda"], left_on=["index","tienda"]).set_axis(df_inventario.index)
df_inventario["rotacion"]=df_inventario["venta"]/df_inventario["sum"]

#========================================================================#
#  ============================== Matriz ============================== #
#========================================================================#
column=0
workbook = xlsxwriter.Workbook(ruta_1)
worksheet = workbook.add_worksheet('rotacion')
for tienda in tqdm(df_distribucion_tiendas.CORTO):
    row=0
    column += 1
    worksheet.write(0, column, tienda)
    for item in df_inventario.index.get_level_values(0).unique():
        worksheet.write(row+1, 0, item)
        #pdb.set_trace()
        unidades = df_inventario[(df_inventario.index == item) & (df_inventario['tienda'] == tienda)]['rotacion'].sum()
        row += 1
        if unidades > 0:
            worksheet.write(row, column, unidades)
        else: worksheet.write(row, column, 0)
workbook.close()

df_Matriz_rotacion=pd.read_excel(ruta_2, index_col=False)
df_Matriz_rotacion=df_Matriz_rotacion.set_index('Unnamed: 0')
tienda=df_Matriz_rotacion.idxmax(axis=1)
rotacion=df_Matriz_rotacion.max(axis=1)
df_Matriz_rotacion["tienda"]=tienda
df_Matriz_rotacion["rotacion"]=rotacion
df_Matriz_rotacion=df_Matriz_rotacion.iloc[:,[24,25]]
df_dis_sobrantes=df_dis_sobrantes.merge(df_Matriz_rotacion, how="left",left_index=True, right_index=True)
df_dis_sobrantes["Destino"]=np.where((df_dis_sobrantes["rotacion"]<=0)|(df_dis_sobrantes["Prueba_sale_1"]=="True")|(df_dis_sobrantes["Prueba_sale_2"]=="True")|(df_dis_sobrantes["Prueba_sale_3"]=="True"),"B034",df_dis_sobrantes["tienda"])
df_dis_sobrantes["Destino"].fillna("B034", inplace=True)
df_dis_sobrantes=df_dis_sobrantes.iloc[:,[0,1,2,3,4,5]]
df_dis_sobrantes["Item"]=df_dis_sobrantes.index

df_dis_sobrantes.to_excel(ruta_3)