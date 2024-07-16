import pandas as pd
from datetime import date
import re
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By


class Web_driver():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = \
            webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def get_gender(self, pag):
        """
        Función para obtener el genero desde la URL 

        parámetros:
            pag(str) : Texto con la url de la página que contiene el genero

        Return: 
            (str): 'hombre', 'mujer' o 'N/A'
        """

        pag = pag.lower()
        if 'hombre' in pag:
            genero = 'hombre'
        elif 'mujer' in pag:
            genero = 'mujer'
        elif 'women' in pag:
            genero = 'mujer'
        elif 'woman' in pag:
            genero = 'mujer'
        elif 'men' in pag:
            genero = 'hombre'
        elif 'man' in pag:
            genero = 'hombre'
        else:
            genero = "N/A"

        return genero

    def arreglar_texto(self, texto_in):
        """
        Función para eliminar espacios y carácteres especiales de los textos

        parámetros: 
            texto_in (str): Texto que se desea editar

        Return:
            (str): Texto editado
        """
        if texto_in is None:
            return None
        else:
            texto_out = re.sub('[^a-zA-Z\s]+', "", texto_in)
            texto_out = texto_out.replace(",", " ")
            texto_out = texto_out.replace(",", "")
            texto_out = texto_out.replace("\n", "")
            texto_out = texto_out.strip()
            texto_out = texto_out.capitalize()
            return texto_out

    def arreglar_moneda(self, valor_in):
        """
        Función para arreglar los precios de los items. Esta función
        elimina los simbolos de moneda, los textos, decimales, puntos, comas, 
        espacios, y todos los caracteres no numericos 

        parámetros:
            valor_in(str): Texto conteniendo el precio de un item

        Return: 
            (str): Texto conteniendo unicamente valores numericos
        """
        if valor_in is None:
            return None
        else:
            valor_out = valor_in.replace(".", "")
            valor_out = valor_out.replace("$", "")
            valor_out = valor_out.replace(",000", "000")
            valor_out = valor_out.replace(",00", "")
            valor_out = valor_out.replace(",", "")
            valor_out = valor_out.replace(" ", "")
            valor_out = re.sub('[^0-9]', "", valor_out)
            return valor_out

    def actualizar_altura(self, x_path):
        altura = self.driver.find_element("xpath", x_path).rect['y']
        self.driver.execute_script(f"window.scrollTo(0, {altura})")


    def true(self):
        print('=============True Scraping==============')
            #================= Definir las páginas a usar ===================
        url=['https://trueshop.co/pages/hombre','https://trueshop.co/pages/mujer']
        paginas = []
        paginas_unisex=[]
        paginas_completo = []
        for genero in url:
            print(genero)
            time.sleep(2)
            self.driver.get(genero)
            x_path='.//div[@class="collection-grid-item"]'
            categorias = self.driver.find_elements(By.XPATH,
                                x_path)
            for categoria in categorias: 
                x_path = './a[@class="collection-grid-item__link"]'
                link = categoria.find_element(By.XPATH,
                                x_path).get_attribute("href")
                regex = re.findall(r'https?:\/\/[\w\-\.]+\.\w{2,5}\/?\w*\/?\/\w*-?\w*-?\w*-?\w*-?\?\w*.\w.\w.\w*.\w*=\w*', link)
                for element in regex: paginas.append(element)
                    
        for pagina in paginas:
            unisex_gen = re.sub('Hombre|Mujer',"Unisex", pagina)
            paginas_unisex.append(unisex_gen)

        paginas_unisex = paginas_unisex + paginas

        for pagina in paginas_unisex:
            if pagina in paginas_completo: continue
            else: paginas_completo.append(pagina)
   
   
        #======= DRIVER PARA RECORRER LAS PAGINAS =======#
        lista_diccionarios = []
        posicion = 0

        for pagina in paginas_completo:
            items_pagina = 0
            time.sleep(2)
            self.driver.get(pagina)
            #Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            #====CATEGORIA====#
            trueshop = requests.get(pagina)
            soup = bs(trueshop.text, 'lxml')
            sopa = soup.find('body')
            categoria = sopa.get('id')

            while True:

                #Botón de scroll
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                #Calculo nueva altura para terminar el scroll
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:

                    x_path = './/div[@class="grid__item small--one-half medium--one-third large-up--one-third"]'
                    items = self.driver.find_elements(By.XPATH, x_path)
                    for item in items:
                        
                        items_pagina +=1
                        posicion +=1
                        #====FOTO====#
                        x_path = './/a[@tabindex="0"]/img'
                        foto = item.find_element(By.XPATH,
                                                x_path).get_attribute("src")

                        #====LINK====#
                        x_path = './/a[@tabindex="0"]'
                        link = item.find_element(By.XPATH,
                                                x_path).get_attribute("href")

                        #====PRECIO ACTUAL====#
                        try:
                            x_path = './/div[@class="grid-view-item__meta"]/span[@class="product-price__price"]'
                            precio_visible = item.find_element(By.XPATH,
                                                            x_path).text
                        except:
                            x_path = """.//div[@class="grid-view-item__meta"]/span[@class="product-price__price product-price__sale"]"""
                            precio_visible = item.find_element(By.XPATH,
                                                            x_path).text 
                        precio_visible = self.arreglar_moneda(precio_visible)               

                        #====PRECIO ANTIGUO====#
                        try:
                            x_path = './/div[@class="grid-view-item__meta"]/s[@class="product-price__price regular"]'
                            precio_antiguo = item.find_element(By.XPATH,
                                                            x_path).text
                        except:
                            precio_antiguo = ""

                        precio_antiguo = self.arreglar_moneda(precio_antiguo)

                        #====NOMBRE====#
                        x_path = './div/div/a'
                        nombre = item.find_element(By.XPATH,
                                                x_path).text

                        nombre = self.arreglar_texto(nombre)

                        #====GENERO====#
                        genero_item = re.findall(r'Hombre|Mujer|Unisex',pagina)[0]

                        lista_diccionarios.append({
                            'fecha': date.today(),
                            'foto': foto,
                            'item' : foto,
                            'posición': posicion,
                            'marca': "True",
                            'pag' : pagina,
                            'nombre': nombre,
                            'precio': precio_visible,
                            'precio descuento': precio_antiguo,
                            'categoria': categoria,
                            'genero' : genero_item,
                            'link': link
                        })

                    break

                last_height = new_height
            print(f'En la pagina {categoria} hay: {items_pagina} ítems en total')

        return pd.DataFrame(
            lista_diccionarios,
            index=range(len(lista_diccionarios))
            )


