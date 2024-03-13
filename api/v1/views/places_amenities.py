#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views.__init__ import app_views
from models.amenity import Amenity
from models.place import Place
from flask import jsonify, abort, request
from models import storage
from os import getenv

cls = Amenity


@app_views.route("/places/<string:place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_ameneties(place_id):
    """ Gets all amenities by place Id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities_obj = place.amenities
    else:
        amenities_obj = []
        for amenity_id in place.aminity_ids:
            amenities_obj.append(storage.get(Amenity, amenity_id))
    amenities = []
    for amenity in amenities_obj:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id=None, amenity_id=None):
    """ Delete place by amenity Id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                break
        else:
            abort(404)
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200
    else:
        for amenity in place.amenity_ids:
            if amenity == amenity_id:
                break
        else:
            abort(404)
        place.amenity_ids.remove(amenity)
        return jsonify({}), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["POST"])
def link_amenity(place_id, amenity_id):
    """ Links a place to an amenity """
    place = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place is None or amenity_obj is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
        place.amenities.append(amenity_obj)
    else:
        for amenity_d in place.amenity_ids:
            if amenity_d == amenity_id:
                return jsonify(amenity.to_dict())
        place.amenity_ids.append(amenity_obj.id)
    place.save()
    return jsonify(amenity_obj.to_dict()), 201
