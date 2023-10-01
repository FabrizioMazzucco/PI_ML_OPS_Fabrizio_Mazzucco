from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
app = FastAPI()
#http://127.0.0.1:8000
review=pd.read_csv('review_funciones.csv') #Abrimos las reseñas
juego=pd.read_csv('juego_funciones.csv') #Abrimos los juegos
item=pd.read_csv('item_funciones.csv') #Abrimos los juegos por usuario
df = pd.read_csv('juego_ml.csv') #Abro el csv de los juegos para ML
df2= pd.read_csv('review_ml.csv') #Abro el csv de las reseñas para ML
@app.get("/")
def idex():
	return {'Mensaje': 'Bienvenidos a mi API. Mi nombre es Fabrizio Mazzucco. Para su uso solo tienen que copiar los links y en el ultimo / poner los valores que desean pero solo funciona con lo que dice, por ejemplo si dice genero no va a funcionar poniendo anio',
            'Anio mas jugado del genero elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/PlayTimeGenre/Genero_deseado',
            'Usuario que mas jugo el genero elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/UserForGenre/Genero_deseado',
            'Juegos con mas resenias en el anio elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/UsersRecommend/Anio_deseado',
            'Juegos con menos resenias en el anio elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/UsersNotRecommend/Anio_deseado',
            'Cantidad de resenias positivas, neutrales y negativas en el anio elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/Sentiment_Analysis/Anio_deseado',
            'Juegos similares al juego elegido': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/recomendacion_juego/Id_juego',
            'Recomendacion de juegos a usuarios': 'https://proyecto-ml-ops-fabrizio-mazzucco.onrender.com/recomendacion_usuario/Id_usuario'}
@app.get("/PlayTimeGenre/{genero_deseado}")
def PlayTimeGenre(genero_deseado:str):
    juegos_genero = juego[juego['genres'] == genero_deseado] # Filtra los juegos por el género deseado
    if juegos_genero.empty:  # Verifica si no hay juegos en el género deseado
        return None
    tabla_completa = juegos_genero.merge(item, left_on='id', right_on='item_id', how='inner') # Combina los datos de los juegos con los datos de los ítems
    tabla_completa['año'] = pd.to_datetime(tabla_completa['release_date']).dt.year# Convierte la columna 'release_date' en formato de fecha y extrae el año
    resumen_por_año = tabla_completa.groupby('año')['playtime_forever'].sum().reset_index() # Resumen: suma las horas jugadas por año
    año_mas_horas_jugadas = resumen_por_año[resumen_por_año['playtime_forever'] == resumen_por_año['playtime_forever'].max()] # Encuentra el año con más horas jugadas
    return (genero_deseado, int(año_mas_horas_jugadas['año'].values[0]))  # Devuelve el año con más horas jugadas como entero

@app.get("/UserForGenre/{genero_buscado}")
def UserForGenre(genero_buscado:str):
    juegos_genero = juego[juego['genres'] == genero_buscado] # Filtra los juegos por el género buscad
    merge_df = juegos_genero.merge(item, left_on='id', right_on='item_id', how='inner')  # Combina los datos de los juegos con los datos de los ítems
    grouped = merge_df.groupby(['user_id', 'release_date', 'genres'])['playtime_forever'].sum().reset_index() # Agrupa por usuario, fecha de lanzamiento y género, sumando las horas jugadas
    max_playtime_users = grouped.loc[grouped.groupby(['release_date', 'genres'])['playtime_forever'].idxmax()] # Encuentra al usuario con más horas jugadas por fecha de lanzamiento y género
    result = {} # Crea un diccionario para almacenar el resultado por año 
    # Itera a través de los usuarios con más horas jugadas
    for _, row in max_playtime_users.iterrows():
        year = pd.to_datetime(row['release_date']).year
        if year not in result:
            result[year] = {'Anio': year, 'Horas': row['playtime_forever']}
        else:
            result[year]['Horas'] += row['playtime_forever']
    max_user = max_playtime_users.iloc[0]['user_id']  # Encuentra al usuario con más horas jugadas en general
    # Formatea el resultado final
    formatted_result = {
        "Usuario con mas horas jugadas para " + genero_buscado: max_user,
        "Horas jugadas": list(result.values())
    }
    
    return formatted_result #Devuelve en diccionario el jugador que mas jugo el genero y las horas jugadas por año

@app.get("/UsersRecommend/{anio_deseado}")
def UsersRecommend(anio_deseado:str):
	df_filtrado = review[review['posted'].str.contains(str(anio_deseado))]   # Filtra las reseñas por el año deseado
	conteo_por_item_id = df_filtrado[df_filtrado['recommend'] == True].groupby('item_id')['recommend'].count() # Cuenta las reseñas recomendadas por juego
	conteo_ordenado = conteo_por_item_id.sort_values(ascending=False) # Ordena los juegos por cantidad de reseñas recomendadas (de mayor a menor)
	top_3_item_id = conteo_ordenado.head(3) # Selecciona los 3 juegos con las mayores cantidades de reseñas recomendadas
	top_3_item_id = top_3_item_id.reset_index() # Reinicia el índice del DataFrame resultante
	top_3_item_id = top_3_item_id.rename(columns={'recommend': 'count'}) # Renombra la columna 'recommend' a 'count'
	resultado_final = top_3_item_id.merge(juego, left_on='item_id', right_on='id', how='inner')[['item_id', 'title', 'count']] # Combina los datos de los juegos mejor recomendados con información del juego (nombre y otros detalles)
	return (resultado_final.drop_duplicates().to_string(index=False))  # Imprime el resultado final sin duplicados y sin mostrar el índice

@app.get("/UsersNotRecommend/{anio_deseado}")
def UsersNotRecommend(anio_deseado:str):
    df_filtrado = review[review['posted'].str.contains(str(anio_deseado))] # Filtra las reseñas por el año deseado
    conteo_por_item_id = df_filtrado[df_filtrado['recommend'] == True].groupby('item_id')['recommend'].count() # Cuenta las reseñas recomendadas por juego
    conteo_ordenado = conteo_por_item_id.sort_values(ascending=True)  # Ordena los juegos por cantidad de reseñas recomendadas de menor a mayor
    bottom_3_item_id = conteo_ordenado.head(3)# Selecciona los 3 juegos con las menores cantidades de reseñas recomendadas
    bottom_3_item_id = bottom_3_item_id.reset_index()# Reinicia el índice del DataFrame resultante
    bottom_3_item_id = bottom_3_item_id.rename(columns={'recommend': 'count'}) # Renombra la columna 'recommend' a 'count'
    resultado_final = bottom_3_item_id.merge(juego, left_on='item_id', right_on='id', how='inner')[['item_id', 'title', 'count']] # Combina los datos de juegos peor recomendados con información del juego (nombre y otros detalles)
    return (resultado_final.drop_duplicates().to_string(index=False)) # Imprime el resultado final sin duplicados y sin mostrar el índice

@app.get("/Sentiment_Analysis/{anio}")
def Sentiment_Analysis(anio:str):
    analyzer = SentimentIntensityAnalyzer() # Crea un objeto SentimentIntensityAnalyzer para análisis de sentimiento
    df_filtrado = review[review['posted'].str.contains(str(anio))]  # Filtra las reseñas por el año deseado
    df_filtrado['sentiment'] = df_filtrado['review'].apply(lambda x: analyzer.polarity_scores(x)['compound']) # Calcula el puntaje de sentimiento (compound) para cada reseña
    # Inicializa contadores para reseñas positivas, negativas y neutrales
    positivos = 0
    negativos = 0
    neutrales = 0
    for compound_score in df_filtrado['sentiment']: # Clasifica las reseñas en positivas, negativas o neutrales
        if compound_score >= 0.05:
            positivos += 1
        elif compound_score <= -0.05:
            negativos += 1
        else:
            neutrales += 1
    # Devuelve un diccionario con la cantidad de reseñas positivas, negativas y neutrales
    return {
        'Positivos': positivos,
        'Negativos': negativos,
        'Neutrales': neutrales
    }

tfidf_vectorizer = TfidfVectorizer() #Creo un vector numerico con la columna de generos para entrenar mi modelo y luego lo entreno
tfidf_matrix = tfidf_vectorizer.fit_transform(df['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix) #Calculo laa similitud del coseno en los juegos

@app.get("/recomendacion_juego/{game_id}")
def recomendacion_juego(game_id: int, top_n=5):
    idx = df.index[df['id'] == game_id].tolist()[0] #Encuentro el indice del juego especifico 
    sim_scores = list(enumerate(cosine_sim[idx])) #Calcula la similitud con el resto de juegos
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) #Ordena los juegos en base a la similitud 
    recommended_indices = [i[0] for i in sim_scores[1:top_n + 1]] #Obtengo los indices de los juegos similares
    return df['title'].iloc[recommended_indices] #Devuelvo los titulos de los juegos similares

@app.get("/recomendacion_usuario/{id}")
def recomendacion_usuario (id): #Creo la funcion y tomo como parametro la id del usuario
    mask= df2['User']== id #Creo una mascara con los registros de la id de usuario
    aux= df2[mask] #Creo una tabla con los registros del usuario al que aplico la recomendacion
    aux.reset_index(drop=True, inplace=True) #Reseteo los indices ya que quedan en diferentes saltos
    recommended_games = recomendacion_juego(game_id=aux['item_id'][0]) #Aqui recomiendo sobre el juego de la primera reseña ya que hay usuarios con muchas reseñas, para recomendar llamo a la funcion anterior
    return recommended_games #Devuelve las recomendaciones