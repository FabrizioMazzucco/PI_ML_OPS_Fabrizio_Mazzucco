<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

<h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

<p align=center><img src=https://static.vecteezy.com/system/resources/previews/020/975/557/original/steam-logo-steam-icon-transparent-free-png.png><p>

**Introducción:**
Este proyecto consiste en crear una API que utiliza un modelo de recomendación para Steam, una plataforma de videojuegos, basado en Machine Learning. El objetivo es crear un sistema de recomendación de videojuegos para usuarios y crear unas funciones que realicen consultas para satisfacer las inquietudes de la empresa entregando asi un MVP (Minimun Viable Product que en español se traduce a Mínimo Producto Viable). Importante responder a la pregunta ¿Qué es una API? Una API (Interfaz de Programación de Aplicaciones) es como un camarero en un restaurante que toma tu pedido, lo comunica a la cocina y te sirve la comida; es un conjunto de reglas que permite a diferentes aplicaciones hablar entre sí y compartir información de manera organizada.

**Pasos del proyecto:**
1. *ETL*

Realizamos un proceso de ETL (Extracción, Transformación y Carga) en el que extrajimos datos de diferentes archivos json, los transformamos en csv y limpiamos segun nuestras necesidades. Existen 5 csv en este trabajo. Primero para las funciones utilizo 'item_funciones.csv' (los juegos con los que cuentan los usuarios y sus horas jugadas), 'juego_funciones.csv' (las especificaciones del juego como genero, precio, etc.) y 'review_funciones.csv' (la reseña que hizo un usuario acerca de un juego). Por ultimo los ultimos dos csv que utilizo para los modelos de recomendacion son 'review_ml.csv' y 'juego_ml.csv'. Aquí hay algo importante que aclarar y es que para un mejor funcionamiento de las funciones y del modelo por cuestiones de pc de bajo rendimiento para un mejor procesamiento y evitar problemas con la pc utilicé menos datos de los que los csv proporcionan esto hace que los modelos y las funciones no anden con cualquier dato que exista en los csv originales sino que andan con algunos datos existentes en los csv con el ETl hecho. La principal herramienta para esta tarea fue Python, librerias Pandas y Random. Json y csv son tipos de archivos donde guardamos nuestra información.

2. *Deployment de la API*

Creamos una API generando 5 funciones para que puedan ser consultadas:

def PlayTimeGenre(genero): Debe devolver año con mas horas jugadas para dicho género.

def UserForGenre(genero): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año. 

def UsersRecommend(año): Devuelve el top 3 de juegos con más reseñas por usuarios para el año dado.  

def UsersNotRecommend(año): Devuelve el top 3 de juegos con menos reseñas por usuarios para el año dado. 

def sentiment_analysis(año): Se devuelve una lista con la cantidad de registros de reseñas
de usuarios que se encuentren categorizados con un análisis de sentimiento en Positivas, Negativas y Neutrales. 

Una vez que ya tenemos nuestra API local la subimos a Render creando asi una página web donde tenemos nuestra API con sus consultas en la nube. Utilizamos librerias Uvicorn y FastApi para la cración de la API, Render para subirla a la red y para las funciones Pandas y NLTK.

3. *EDA*

Realizamos un analisis exploratorio de datos con el objetivo de obtener insights, identificar patrones, tendencias y relaciones, y así tomar decisiones fundamentadas en base a la información obtenida. Intentando asi obtener alguna pista para crear nuestro modelo de ML. Las herramientas utilizadas fueron:  Pandas, Matplotlib, Wordcloud y NLTK.

4. *Modelo de Machine Learning*

Realizamos un modelo de Machine Learning para generar recomendaciones de juegos en base a los géneros del juego, generando en cada juego un vector numérico para la columna género y asi calculando la similitud del coseno entre el género de un juego y del resto de juegos para recomendar juegos de los mismos géneros ya que van a tener un vector muy similar entre ambos juegos. En el segundo modelo la metodología es revisar las reseñas y si ve que el usuario recomienda un juego utiliza el mismo modelo anterior sobre el juego recomendado. Mi idea era crear un modelo utilizando otras columnas de la tabla como especificaciones, tags o precio pero por cuestiones de rendimiento no pude usarlas. Vuelvo a aclarar solo podemos usar los datos específicos de los csv ya transformados. El problema con los modelos es que estan todos los usuarios que reseñaron juegos pero no estan todos los juegos así que podemos ingresar un usuario existente pero el juego reseñado no existe en la tabla juegos por lo que no va a reseñar nada.  

def recomendacion_juego(id de producto): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.


def recomendacion_usuario(id de usuario): Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario. 

La herramienta utilizada fue: Scikit-Learn con las librerias: TfidfVectorizer, linear_kernel, cosine_similarity Tambien son consultables en la API

**Para finalizar**

Aqui dejo algunos ejemplos de datos que estan en los csv reducidos que podemos usar en los modelos de recomendación, podemos usar otros usuarios y juegos que se encuentren en los csv de ML siempre y cuando sean compatibles los datos. También aclaramos que la API esta en construcción ya que el objetivo del trabajo era entregar el MVP(Mínimo Producto Viable) por lo que puede andar medio lenta y tener errores de estructura.

Ejemplos de usuarios con juegos existentes en la tabla: SALTTHEW0UND, evcentric, doctr, GodLoveGuru, Ghoustik

Ejemplos id de juegos: 359450, 761140, 643980, 670290, 767400

Generos que podemos utilizar: Action, Casual, Indie, Simulation, Strategy, Free to Play, RPG, Sports, Adventure, nan, Racing, Early Access, Massively Multiplayer, Animation &amp; Modeling, Video Production, Utilities, Web Publishing, Education, Software Training, Design &amp; Illustration, Audio Production, Photo Editing, Accounting. IMPORTANTE: Hay géneros que tal vez nos den error por la falta de datos.

*Link de la API*: https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/

*Video explicativo*: https://www.youtube.com/watch?v=7S7lbN0EPJU&t=7s

*Mi linkedin*: www.linkedin.com/in/fabrizio-mazzucco-403b0825a
