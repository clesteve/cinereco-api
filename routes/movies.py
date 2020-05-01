from application import application
from flask import jsonify, request
from models import movies


@application.route('/movies/<page>', methods=["POST"])
def getMovies(page):
    moviefilter = request.json
    data = movies.getAll(moviefilter=moviefilter, page=int(page))
    return jsonify(data)


@application.route('/movies/trailer/<id>')
def getTrailer(id):
    return jsonify(movies.getTrailer(id))


@application.route('/reco', methods=["POST"])
def getRecos():
    recos = movies.getRecos(
        request.json["liked"], request.json["disliked"], request.json["watched"])
    return jsonify(recos)
