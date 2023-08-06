# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from schemas import MovieSchema, GenreSchema, DirectorSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
movie_ns = api.namespace('movies')
genre_ns = api.namespace('genre')
director_ns = api.namespace('director')

movie_schemas = MovieSchema(many=True)
movie_schema = MovieSchema()
genre_schemas = GenreSchema(many=True)
genre_schema = GenreSchema()
director_schemas = GenreSchema(many=True)
director_schema = GenreSchema()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movie_ns.route('/')
class MovieViews(Resource):

    def get(self):
        data = Movie.query.all()

        director_id = request.args.get('director_id')
        if director_id:
            data = Movie.query.filter_by(director_id=director_id).all()

        genre_id = request.args.get('genre_id')
        if genre_id:
            data = Movie.query.filter_dy(genre_id=genre_id).all()

        return MovieSchema.dump(data)

    def post(self):
        data = request.json
        try:
            db.session.add(Movie(**data))
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 201


@movie_ns.route('/<int:uid>')
class MovieViews(Resource):
    def get(self, uid):
        data = Movie.query.get(uid)
        return MovieSchema.dump(data)

    def put(self, uid):
        data = request.json

        try:
            db.session.query(Movie).filter(Movie.id == uid).update(data)
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, uid):
        try:
            db.session.query(Movie).filter(Movie.id == uid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@genre_ns.route('/')
class GenreViews(Resource):

    def get(self):
        data = Genre.query.all()

        name = request.args.get('name')
        if name:
            data = Genre.query.filter_by( name= name).all()

        genre_id = request.args.get('genre_id')
        if genre_id:
            data = Genre.query.filter_dy(genre_id=genre_id).all()

        return GenreSchema.dump(data)

    def post(self):
        data = request.json
        try:
            db.session.add(Genre(**data))
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 201


@genre_ns.route('/<int:uid>')
class GenreViews(Resource):
    def get(self, uid):
        data = Genre.query.get(uid)
        return GenreSchema.dump(data)

    def put(self, uid):
        data = request.json

        try:
            db.session.query(Genre).filter(Genre.id == uid).update(data)
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, uid):
        try:
            db.session.query(Genre).filter(Genre.id == uid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

# !!!!!!!!!!!!!!!!!!
@director_ns.route('/')
class DirectorViews(Resource):

    def get(self):
        data = Director.query.all()

        name = request.args.get('name')
        if name:
            data = Director.query.filter_by( name= name).all()

        genre_id = request.args.get('genre_id')
        if genre_id:
            data = Director.query.filter_dy(genre_id=genre_id).all()

        return DirectorSchema.dump(data)

    def post(self):
        data = request.json
        try:
            db.session.add(Director(**data))
            db.session.commit()
            return 'Данные добавлены', 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 201


@director_ns.route('/<int:uid>')
class DirectorViews(Resource):
    def get(self, uid):
        data = Director.query.get(uid)
        return DirectorSchema.dump(data)

    def put(self, uid):
        data = request.json

        try:
            db.session.query(Director).filter(Director.id == uid).update(data)
            db.session.commit()
            return 'Данные обновлены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, uid):
        try:
            db.session.query(Director).filter(Director.id == uid).delete()
            db.session.commit()
            return 'Данные удалены', 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


if __name__ == '__main__':
    app.run(debug=True)
