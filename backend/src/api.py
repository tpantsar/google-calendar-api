"""
API Blueprint and API resources
"""

from flask import Blueprint
from flask_restful import Api

# Import collections
from resources.calendar import CalendarList, CalendarListId
from resources.event import EventItem, EventList

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp, catch_all_404s=True)

# Add resources
api.add_resource(CalendarList, "/calendars/", methods=["GET"])
api.add_resource(CalendarListId, "/calendars/id/", methods=["GET"])

api.add_resource(EventList, "/events/<calendar_id>/", methods=["GET", "POST"])
api.add_resource(
    EventItem,
    "/events/<calendar_id>/<event_id>/",
    methods=["GET", "PUT", "DELETE"],
)
