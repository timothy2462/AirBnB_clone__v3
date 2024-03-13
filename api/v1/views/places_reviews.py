#!/usr/bin/python3
"""
A new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views.__init__ import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from models import storage

cls = Review


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Get all reviews by place Id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    reviews = []
    for review in obj.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id=None):
    """ Get all reviews by review Id """
    if review_id is not None:
        obj = storage.get(cls, review_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """ Deletes a review by Id """
    obj = storage.get(cls, review_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id=None):
    """ Creates a review"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "text" not in my_dict:
        abort(400, "Missing text")
    if "user_id" not in my_dict:
        abort(400, "Missing user_id")
    texts = my_dict["text"]
    pla = my_dict['user_id']
    obj = storage.get(User, pla)
    if obj is None:
        abort(404)
    obj = cls(text=texts, place_id=place_id, user_id=pla)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=["PUT"])
def update_review(review_id):
    """ Updates a review """
    obj = storage.get(cls, review_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'updated_at' or k == 'place_id':
            continue
        if k == 'id' or k == 'created_at' or k == 'user_id':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
