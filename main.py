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
    movie = models.Movie.create(**movie.model_dump())
    return movie

# @app.delete("/movies/{movie_id}", response_model=schemas.Movie)
# def delete_movie(movie_id: int):
#     movie = models.Movie.get(models.Movie.id == movie_id)
#     if movie is None:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     movie.delete_instance()
#     return list(models.Movie.select())

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    movie = models.Movie.get_or_none(models.Movie.id == movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.delete_instance()
    return list(models.Movie.select())
#newMovie = models.Movie.create(title="Fight Club", year=1999, director="David Fincher", description="")

@app.get("/actors", response_model=List[schemas.Actor])
def get_actors():
    return list(models.Actor.select())

@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int):
    actor = models.Actor.get(models.Actor.id == actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.Actor):
    newActor = models.Actor.create(**actor.model_dump())
    return newActor

@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_actor(movie_id: int, actor: schemas.ActorBase):
    movie = models.Movie.get(models.Movie.id == movie_id)
    actor = models.Actor.get((models.Actor.name == actor.name) & (models.Actor.surname == actor.surname))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    movie.actors.add(actor)
    movie.save()
    return movie






