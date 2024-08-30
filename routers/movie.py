from fastapi import Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

def get_movie_by_id(id):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    return result;

@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    status_code = 200

    if not result:
        status_code = 404
        result = { "message": "Movie not found" }

    return JSONResponse(status_code=status_code, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5,max_length=15)) -> Movie:
    db = Session()
    result = MovieService(db).get_by_category(category)
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)

    return JSONResponse(status_code=201, content={"message": "Película agregada correctamente"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict: 
    db = Session()
    MovieService(db).update_movie(id, movie)
   
    return JSONResponse(status_code=200, content={"message": "Película modificada correctamente"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    found_movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    db.delete(found_movie)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Película eliminada correctamente"})