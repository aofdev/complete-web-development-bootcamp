
from pymongo.collection import Collection
from entities.movie import Movie
from bson.objectid import ObjectId
from typing import Dict
from pprint import pprint


class MovieRepository():
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_all(self):
        return [self.map_raw_to_movie(movie_raw)
                for movie_raw in self.collection.find()]

    def find_by_id(self, movie_id: str):
        movie_raw = self.collection.find_one({"_id": ObjectId(movie_id)})
        if (movie_raw is None):
            raise NoMovieError
        return self.map_raw_to_movie(movie_raw)

    def create(self, movie: Movie):
        inserted_result = self.collection.insert_one(
            movie.dict(exclude_unset=True))
        inserted_id = str(inserted_result.inserted_id)
        return inserted_id

    def update(self, movie_id: str, movie: Movie):
        updated_result = self.collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": movie.dict(exclude_unset=True)})
        if updated_result.modified_count == 0:
            raise NoMovieUpdateError
        return movie_id

    def delete(self, movie_id: str):
        deleted_result = self.collection.delete_one(
            {"_id": ObjectId(movie_id)})
        if deleted_result.deleted_count == 0:
            raise NoMovieDeleteError
        return movie_id

    def map_raw_to_movie(self, movie_raw: Dict):
        return Movie(**{
            "id": str(self.is_key_in_dict(key="_id", movie_raw=movie_raw)),
            "name": self.is_key_in_dict(key="name", movie_raw=movie_raw),
            "genres": self.is_key_in_dict(key="genres", movie_raw=movie_raw),
            "poster": self.is_key_in_dict(key="poster", movie_raw=movie_raw),
            "synopsis": self.is_key_in_dict(key="synopsis", movie_raw=movie_raw),
            "release_date": self.is_key_in_dict(key="release_date", movie_raw=movie_raw),
        })

    def is_key_in_dict(self, key: str, movie_raw: Dict):
        return movie_raw[key] if key in movie_raw else None


class NoMovieError(Exception):
    """Raised when the no movie is found from db"""
    pass


class NoMovieUpdateError(Exception):
    """Raised when failed to update movie in db"""
    pass


class NoMovieDeleteError(Exception):
    """Raised when failed to delete movie in db"""
    pass
