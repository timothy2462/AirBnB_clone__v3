#!/usr/bin/python3
'''Contains the states view for the API.'''

from api.v1.views.__init__ import app_views
from models.state import State
from flask import jsonify, abort, request
from models import storage

cls = State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id=None):
    """ Get all states or a single state by ID """
    if state_id is not None:
        obj = storage.get(cls, state_id)
        if obj is None:
            abort(404)
        else:
            return jsonify(obj.to_dict())
    else:
        objs = storage.all(cls)
        my_list = []
        for obj in objs.values():
            my_list.append(obj.to_dict())
        return jsonify(my_list)


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ Deletes a state by ID """
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Adds a new state to States """
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "name" not in my_dict:
        abort(400, "Missing name")
    state_name = my_dict["name"]
    obj = cls(name=state_name)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """ Updates a State by ID """
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
