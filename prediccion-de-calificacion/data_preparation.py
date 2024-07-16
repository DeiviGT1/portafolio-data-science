# Importación de librerías necesarias
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import warnings
from unidecode import unidecode

# Ignorar advertencias
warnings.filterwarnings("ignore")

#################################################################### Descripción ########################################################################
#########################################################################################################################################################

# Este script procesa datos relacionados con despachos de artículos y su maestro, realizando operaciones como consultas SQL,
# limpieza y transformación de datos en DataFrames de Pandas, y combinación de datos de diferentes fuentes.

########################################################################################################################################################
########################################################################################################################################################



# Definición de credenciales para conexión a base de datos
usuario = "XXX"
contrasena = r"XXX"

########################################################################################################################################################
# Clase para manejo de consultas SQL
class SQL():
    def __init__(self, cnn_str) -> None:
        self.engine = create_engine(cnn_str)
   

    def tabla_des(self):
        """
        Consulta la tabla de despachos
        """
        SQL = """
            XXX
        """
        return pd.read_sql(SQL, self.engine) # Ejecutar la consulta y retornar los resultados como un DataFrame de pandas
 
def carga_datos(mes_exh=False, columns_to_remove=None):
    tabla_items = pd.read_csv(r"XXX", sep = '\t', encoding = 'XXX')

    # Preprocesamiento de datos en el DataFrame de maestro de items
    tabla_items = tabla_items.drop(['Desc. item', 'TIPO', 'LARGO', 'MARCA', 'Desc. ext. 1 detalle', 'Costo prom. uni.', 'Tipo inventario', 'CLUSTER CURVAS'], axis=1)  # Eliminar columnas no necesarias
    tabla_items.columns = ['item', 'genero', 'categoria', 'color', 'estetica', 'base_tela', 'silueta','sub_categoria', 'precio']  # Renombrar columnas
    for col in list(tabla_items.select_dtypes(include=['object']).columns):
        tabla_items[col] = tabla_items[col].str.lower().str.rstrip()  # Convertir texto a minúsculas y eliminar espacios al final
        tabla_items[col] = tabla_items[col].apply(lambda x: unidecode(x))  # Eliminar caracteres especiales
    tabla_items = tabla_items[(tabla_items['genero'] == 'hombre') | (tabla_items['genero'] == 'mujer')]  # Filtrar por género 'hombre' o 'mujer'

    tabla_items['base_tela'] = tabla_items['base_tela'].replace('dril', 'drill')
    
    tabla_items = procesamiento_tabla(df=tabla_items)
    
    if mes_exh:
        tabla_items['fecha_exhibicion'] = mes_exh
        tabla_items['fecha_exhibicion'] = tabla_items['fecha_exhibicion'].astype(object)

    if columns_to_remove:
            for column in columns_to_remove:
                if column in tabla_items.columns:
                    tabla_items.drop(column, axis=1, inplace=True)
    
    return tabla_items
   
def procesamiento_tabla(df):
    
    df['precio'] = df['precio'].str.replace('$', '').str.replace(',', '').astype(float)  # Eliminar símbolos de moneda y convertir a tipo numérico
    # Definir condiciones y opciones para transformar la columna 'estetica'
    conditions = [
        df['estetica'].str.contains('camuflado'),
        (df['estetica'].str.contains('lavanderia')) | (df['estetica'].str.contains('tie dye')),
        df['estetica'].str.contains('bloque'),
        (df['estetica'].str.contains('ilustracion')) | (df['estetica'].str.contains('oso')),
        df['estetica'].str.contains('texto'),
        df['estetica'].str.contains('print'),
        (df['estetica'].str.contains('fotografia')) | (df['estetica'].str.contains('poster')),
        df['estetica'].str.contains('calavera'),
        df['estetica'].str.contains('rayas'),
        df['estetica'].str.contains('numero'),
        df['estetica'].str.contains('brillo'),
        (df['estetica'].str.contains('basico') | df['estetica'].str.contains('icono') )
    ]
    choices = [
        'camuflado',
        'lavanderia',
        'bloque',
        'ilustracion',
        'texto',
        'print',
        'fotografia',
        'calavera',
        'rayas',
        'numero',
        'brillo',
        'basico'
    ]
    df['estetica'] = np.select(conditions, choices, default='basico')
    # Ajustar valores en la columna 'sub_categoria'
    try:
        conditions = [
            (df['sub_categoria'] == ""),
            
            (df['sub_categoria'].str.contains('over')),
            (df['sub_categoria'].str.contains('crop')),
            (df['sub_categoria'].str.contains('tank')),
            (df['sub_categoria'].str.contains('camiseta')),
            
            (df['sub_categoria'].str.contains('top')),
            (df['sub_categoria'].str.contains('body')),
            (df['sub_categoria'].str.contains('interno')),
            
            ]
        choices = [
            'no aplica',
            'over',
            'crop',
            'tank',
            'camiseta',
            'top',
            'body',
            'interno'
        ]
        df['sub_categoria'] = np.select(conditions, choices, default='no aplica')

            # Ajustar valores en la columna 'base_tela'
        conditions = [ 
            ((df['base_tela'] == "")|(df['base_tela'].str.contains('sintetico'))),
            (df['base_tela'].str.contains('burda')),
            (df['base_tela'].str.contains('punto')),
            (df['base_tela'].str.contains('rib')),
            (df['base_tela'].str.contains('moda')),
        ]
        choices = [
            'no aplica',
            'burda',
            'punto',
            'rib',
            'moda',
        ]
        df['base_tela'] = np.select(conditions, choices, default='no aplica')
    except:
        pass
    # Ajustar valores en la columna 'silueta'
    conditions = [
        (df['silueta'] == ""),
        ((df['silueta'] == 'super skinny')|(df['silueta'].str.contains('ajustado'))),
        ((df['silueta'] == 'skinny')|(df['silueta'] == 'semiajustado')),
        (df['silueta'].str.contains('box fit')),
        ((df['silueta'] == 'over')|(df['silueta'] == 'amplio')),
        (df['silueta'] == 'regular'),
    ]
    choices = [
        'no aplica',
        'ajustado',
        'semiajustado',
        'box fit',
        'amplio',
        'regular',
    ]
    df['silueta'] = np.select(conditions, choices, default='no aplica')
    # Ajustar valores en la columna 'color'
    conditions = [
        (df['color'] == 'blanco'),
        (df['color'] == 'negro'),
        ((df['color'] == 'marfil') | (df['color'] == 'beige')),
        (df['color'] == 'gris'),
    ]
    choices = [
        'blanco',
        'negro',
        'marfil',
        'gris',
    ]
    df['color'] = np.select(conditions, choices, default='color')

    return df

def main ():
    # Configuración de la conexión a la base de datos

    cnn_str_dw = 'XXX'
    SQL_cnn_dw = SQL(cnn_str_dw)
    tabla_des = SQL_cnn_dw.tabla_des()

    tabla_items = carga_datos()
    
    # Combinar el DataFrame de maestro de items con la tabla de despachos
    tabla_items = tabla_items.merge(
        tabla_des,
        how = 'inner',
        on = 'item'
    ).sort_values(by=['item', 'fecha_exhibicion'])

    # Normalizar valores en la columna 'base_tela'
    
    # Lectura del archivo de calificación y ajuste de columnas
    calificacion = pd.read_excel("XXX").iloc[:, :2]
    calificacion.columns = ['item', 'calificacion']

    # Combinar el DataFrame de maestro de items con el DataFrame de calificación
    tabla_items = tabla_items.merge(
        calificacion,
        how = 'inner',
        on = 'item'
    )

    #convert fecha_exhibicion to month
    tabla_items['fecha_exhibicion'] = pd.to_datetime(tabla_items['fecha_exhibicion'])
    tabla_items = tabla_items[tabla_items['fecha_exhibicion'] > '2020-01-01']
    tabla_items['fecha_exhibicion'] = tabla_items['fecha_exhibicion'].dt.month
    tabla_items['fecha_exhibicion'] = tabla_items['fecha_exhibicion'].astype('object')
    

    tabla_items.index = tabla_items['item']  # Establecer el índice en la columna 'item'
    tabla_items.drop(columns=['item'], inplace=True)  # Eliminar la columna 'item'

    return tabla_items # Retornar el DataFrame procesado