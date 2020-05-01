from application import application
import pandas as pd
import requests
import re
import numpy as np
from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors


movie_api = "http://www.omdbapi.com/?apikey={}".format(
    application.config["API_KEY"])

df_movies = pd.read_csv(
    "data/movies.csv")

w = np.load("data/gensim_model.npy")
movie_embedding_size = w.shape[1]


def getAll(nb=3, page=0, idlist=None, moviefilter=None):
    if not idlist and not moviefilter:
        movies = df_movies.sort_values(
            by="count", ascending=False).iloc[page*nb: (page + 1)*nb].to_dict(orient="records")
    if idlist:
        movies = df_movies[df_movies['movieId'].isin(idlist)].sort_values(
            by="count", ascending=False).to_dict(orient="records")

    if moviefilter:
        df_filtered = df_movies.copy()
        for column, value in moviefilter.items():
            df_filtered = df_filtered[df_filtered[column].str.contains(
                value, case=False)]

        movies = df_filtered.sort_values(
            by="count", ascending=False).iloc[page*nb: (page + 1)*nb].to_dict(orient="records")

    for mv in movies:
        # Date to string
        mv["date"] = str(int(mv["date"])) if mv["date"] == mv["date"] else ""
        # Separate date from title
        mv["title"] = re.split(r"\([0-9]{4}\)", mv["title"])[0]
        # Remove things between parentheses
        mv["title"] = re.sub(
            r"\([^)]{1,}\)", "", mv["title"]).strip()
        # "Castle in the sky, The" => "The Castle in the sky"
        if ", The" in mv["title"][-6:]:
            mv["title"] = "The " + mv["title"][:-5]
        # "Beautiful Mind, A" => "A Beautiful Mind"
        if ", A" in mv["title"][-5:]:
            mv["title"] = "A " + mv["title"][:-3]

        mv["id"] = mv["movieId"]
        mv["data"] = requests.get(
            movie_api + "&t={}&type=movie&y={}".format(mv["title"], mv["date"])).json()

    return movies


def getRecos(liked, disliked, watched, threshold=1000):

    liked = [str(l) for l in liked]
    disliked = [str(l) for l in disliked]

    watched = [str(w) for w in watched if str(
        w) not in liked and str(w) not in disliked]

    df_restr = df_movies[~df_movies["movieId"].isin(watched)].sort_values(
        by="count", ascending=False)

    kv = WordEmbeddingsKeyedVectors(movie_embedding_size)
    kv.add(
        df_restr['movieId'].apply(str).values,
        w[df_restr.movieId]
    )

    idlist = [int(x[0])
              for x in kv.most_similar(positive=liked, negative=disliked, restrict_vocab=4000)]

    return getAll(idlist=idlist)


def getTrailer(movieId):
    try:
        movie = df_movies[df_movies["movieId"] == int(movieId)].iloc[0]
        date = str(int(movie['date'])
                   ) if movie["date"] == movie["date"] else ""
        youtube_id = requests.get("https://www.youtube.com/results?search_query={}+trailer&pbj=1".format(movie['title'] + " " + date)
                                  ).content.split(b'href="/watch?v=')[1][:11].decode("utf-8")

        return 'https://www.youtube.com/embed/' + youtube_id

    except Exception as err:
        print(err)
        # print(resp.json())
        return ''
