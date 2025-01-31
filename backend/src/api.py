"""
API Blueprint and API resources
"""

from flask import Blueprint, Response
from flask_restful import Api

# Import collections
from src.resources.calendar import CalendarList, CalendarListId
from src.resources.event import EventItem, EventList

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint)


@api_blueprint.after_request
def after_request(response: Response) -> Response:
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    header["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


# Add resources
api.add_resource(CalendarList, "/calendars/", methods=["GET"])
api.add_resource(CalendarListId, "/calendars/id/", methods=["GET"])

api.add_resource(EventList, "/events/<calendar_id>/", methods=["GET", "POST"])
api.add_resource(
    EventItem,
    "/events/<calendar_id>/<event_id>/",
    methods=["GET", "PUT", "DELETE"],
)
