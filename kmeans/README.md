<h1 align="center"> KMeans </h1>

<p align="center">
  <img src="./assets/Kmeans.gif" alt="custom image"/>
</p>

<br>
<br>
<h2 align="center">🏁 El proyecto se encuentra terminado 🏁 </h2>

<h4> 🔨 Calificar los ítems de una forma cuantitativa automática con K-means 🔨 </h4>


## 📁 Acceso al proyecto

**Este proyecto puede ser descargado como archivo ZIP o realizando una conexión con el http por medio de git**

<br>

## 🛠️ Abre y ejecuta el proyecto

**Se puede correr el archivo desde la terminal en cualquier sistema operativo**

<br>
<br>

## ✅ Tecnologias usadas

- **Python**<br>
- **Scikit-learn**<br>
- **Numpy**<br>
- **Pandas**<br>
- **Scipy**<br>
<br>

`Ventajas` :
- El principio es simple, la implementación es fácil y la velocidad de convergencia es rápida.
- Hay pocos parámetros para ajustar, y generalmente solo el número de clúster K necesita ser ajustado.
- El numero de clasificaciones puede cambiar dependiendo de la necesidad en su momento
- Calificar ítems por medio de sus ventas en un tiempo determinado

<br>

 `Tipos de datos` : 
 - Se decide usar 3 clusters para la optmizacion del modelo y obtener los resultados mas exactos posibles
 
<div align="center">
  <img src="./assets/Clusters.png" alt="custom image" style="width:40%;position:relative; top:-3rem"/>
  <img src="./assets/Modelo.png" alt="custom image" style="width:40%"/>
</div>

<br>

`Analisis por categoria` :
Teniendo en cuenta que cada categoria tiene ventas y unidades despachadas muy diferentes, el modelo tiene en cuenta esta diferencia para crear unos centroides y una categorizacion distinto para cada uno

<div align="center">
  <img src="./assets/categoria.png" alt="custom image" />
</div>

<br>

`Lote` : 
Las categorias grandes como Hombre tank y Hombre camiseta tienen diferencias en dos subdivisiones del lote, cambiando fuertemente los resultados del modelo asi que se ha dividido estas categorias en dos lotes diferentes

<div align="center">
  <img src="./assets/lote.png" alt="custom image" />
</div>
