"""
API Blueprint and API resources
"""

from flask import Blueprint
from flask_restful import Api

# Import collections
from resources.calendar import CalendarCollection, CalendarIdCollection

# from resources.event import EventCollection, EventItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# Add resources
api.add_resource(CalendarCollection, "/calendars/", methods=["GET"])
api.add_resource(CalendarIdCollection, "/calendars/id/", methods=["GET"])
