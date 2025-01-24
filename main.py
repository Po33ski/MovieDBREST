from fastapi import FastAPI, HTTPException
from typing import List

import models
import schemas

app = FastAPI()
#movies methods:
@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    #movie = models.Movie.get(models.Movie.id == movie_id)
    movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    movie = models.Movie.create(**movie.model_dump())
    return movie


@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.delete_instance()
    return movie

#actors methods:
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

@app.delete("/actors/{actor_id}", response_model=schemas.Actor)
def delete_movie(actor_id: int):
    actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    actor.delete_instance()
    return actor

@app.post("/movies/{movie_id}/actors", response_model=schemas.Movie)
def update_actor(movie_id: int, actor: schemas.ActorBase):
    movie = models.Movie.filter(models.Movie.id == movie_id).first()
    actor = models.Actor.get((models.Actor.name == actor.name) & (models.Actor.surname == actor.surname))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    movie.actors.add(actor)
    movie.save()
    return movie






