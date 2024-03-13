#!/usr/bin/python3
"""
Contains the blueprint for the API
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


import api.v1.views.index
import api.v1.views.states
import api.v1.views.cities
import api.v1.views.amenities
import api.v1.views.users
import api.v1.views.places
import api.v1.views.places_reviews
import api.v1.views.places_amenities
