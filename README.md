<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

<h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

<p align=center><img src=https://static.vecteezy.com/system/resources/previews/020/975/557/original/steam-logo-steam-icon-transparent-free-png.png><p>

**Introducción:**
Este proyecto consiste en crear una API que utiliza un modelo de recomendación para Steam, una plataforma de videojuegos, basado en Machine Learning. El objetivo es crear un sistema de recomendación de videojuegos para usuarios.

**Pasos del proyecto:**
1. *ETL*

Realizamos un proceso de ETL (Extracción, Transformación y Carga) en el que extrajimos datos de diferentes archivos json, los transformamos en csv y limpiamos segun nuestras necesidades. Existen 5 csv en este trabajo. Primero para las funciones utilizo 'item_funciones.csv' (los juegos con los que cuentan los usuarios y sus horas jugadas), 'juego_funciones.csv' (las especificaciones del juego como genero, precio, etc.) y 'review_funciones.csv' (la reseña que hizo un usuario acerca de un juego). Por ultimo los ultimos dos csv que utilizo para los modelos de recomendacion son 'review_ml.csv' y 'juego_ml.csv'. Aquí hay algo importante que aclarar y es que para un mejor funcionamiento de las funciones y del modelo por cuestiones de pc de bajo rendimiento para un mejor procesamiento y evitar problemas con la pc utilicé menos datos de los que los csv proporcionan esto hace que los modelos y las funciones no anden con cualquier dato que exista en los csv originales sino que andan con algunos datos existentes en los csv con el ETl hecho. La principal herramienta para esta tarea fue Python, librerias Pandas y Random.

2. *Deployment de la API*

Creamos una API generando 5 funciones para que puedan ser consultadas:

def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año. 
def UsersRecommend( año : int ): Devuelve el top 3 de juegos MáS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales) 
def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos) 
def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. 
Una vez que ya tenemos nuestra API local la subimos a Render creando asi una página web donde tenemos nuestra API con sus consultas en la nube. Utilizamos librerias Uvicorn y FastApi para la cración de la API, Render para subirla a la red y para las funciones Pandas y NLTK.

3. *EDA*

Realizamos un analisis exploratorio de datos con el objetivo de obtener insights, identificar patrones, tendencias y relaciones, y así tomar decisiones fundamentadas en base a la información obtenida. Intentando asi obtener alguna pista para crear nuestro modelo de ML. Las herramientas utilizadas fueron: Numpy, Pandas, Matplotlib, Wordcloud, NLTK.

4. *Modelo de Machine Learning*

Realizamos un modelo de Machine Learning para generar recomendaciones de juegos en base a los géneros del juego, calculando la similitud del coseno entre el género de un juego y del resto de juegos recomienda juegos de los mismos géneros. En el segundo modelo la metodología es revisar las reseñas y si ve que el usuario recomienda un juego le recomienda juegos parecidos utilizando también la similitud del coseno en los géneros del juego recomendado. Mi idea era crear un modelo utilizando otras columnas de la tabla como especificaciones, tags o precio pero por cuestiones de rendimiento no pude usarlas. Vuelvo a aclarar solo podemos usar los datos específicos de los csv procesados. El problema con los modelos es que estan todos los usuarios que reseñaron juegos pero no estan todos los juegos así que podemos ingresar un usuario existente pero el juego reseñado no existe en la tabla juegos por lo que no va a reseñar nada.  

def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.


def recomendacion_usuario( id de usuario ): Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario. 

La herramienta utilizada fue: Scikit-Learn con las librerias: TfidfVectorizer, linear_kernel, cosine_similarity Tambien son consultables en la API


*Aqui dejo algunos ejemplos de datos que estan en los csv reducidos que podemos usar en los modelos de recomendación*

Ejemplos de usuarios con juegos existentes en la tabla: SALTTHEW0UND, evcentric, doctr, GodLoveGuru, Ghoustik

Ejemplos id de juegos: 359450, 761140, 643980, 670290, 767400

Generos que podemos utilizar: Action, Casual, Indie, Simulation, Strategy, Free to Play, RPG, Sports, Adventure, nan, Racing, Early Access, Massively Multiplayer, Animation &amp; Modeling, Video Production, Utilities, Web Publishing, Education, Software Training, Design &amp; Illustration, Audio Production, Photo Editing, Accounting. IMPORTANTE: Hay generos que tal vez nos den error por la falta de datos.

*Link de la API*: https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/

*Video explicativo*: https://www.youtube.com/watch?v=7S7lbN0EPJU&t=7s

*Mi linkedin*: www.linkedin.com/in/fabrizio-mazzucco-403b0825a
