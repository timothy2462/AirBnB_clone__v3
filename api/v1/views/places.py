#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views.__init__ import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from models import storage

cls = Place


@app_views.route("/cities/<string:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """ Get a list of places for a specific city """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    places = []
    for place in obj.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id=None):
    """ Get a specific place by id """
    if place_id is not None:
        obj = storage.get(cls, place_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_place(place_id):
    """ Deletes a specific place by place_id """
    obj = storage.get(cls, place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id=None):
    """Creates a Place"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "name" not in my_dict:
        abort(400, "Missing name")
    if "user_id" not in my_dict:
        abort(400, "Missing user_id")
    names = my_dict["name"]
    pla = my_dict['user_id']
    obj = storage.get(User, pla)
    if obj is None:
        abort(404)
    obj = cls(name=names, city_id=city_id, user_id=pla)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"])
def update_place(place_id):
    """ Update a specific place by place_id """
    obj = storage.get(cls, place_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'updated_at' or k == 'city_id':
            continue
        if k == 'id' or k == 'created_at' or k == 'user_id':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
