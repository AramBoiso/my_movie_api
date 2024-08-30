from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie(self, id):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie
    
    def get_by_category(self, category):
        movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movies
    
    def create_movie(self, movie: Movie):
       new_movie =  MovieModel(**movie.model_dump())
       self.db.add(new_movie)
       self.db.commit()
       return
    
    def update_movie(self, id: int, movie: Movie):
        found_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if found_movie:
          found_movie.title = movie.title
          found_movie.overview = movie.overview
          found_movie.year = movie.year
          found_movie.rating = movie.rating
          found_movie.category = movie.category
          self.db.commit()

    def delete_movie(self, id: int):
        found_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(found_movie)
        self.db.commit()