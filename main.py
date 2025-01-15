from fastapi import FastAPI, HTTPException
from typing import List

import models
import schemas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    movie = models.Movie.get(models.Movie.id == movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.Movie):
    newMovie = models.Movie.create(title=movie.title, year=movie.year, director=movie.director, description=movie.description)
    newMovie.save()
    movie = models.Movie.create(**movie.model_dump())
    return movie





# @app.get("/movies/", response_model=List[schemas.Movie])
# def get_movies():
#     list_of_movies = List[models.Movie.select()]
#     return list_of_movies
#     for movie in list_of_movies.select():
#         print(movie.title, movie.year, movie.director, movie.description)
#         for actor in movie.actor:
#             print(actor.name, actor.surname)


#newMovie = models.Movie.create(title="Fight Club", year=1999, director="David Fincher", description="")
