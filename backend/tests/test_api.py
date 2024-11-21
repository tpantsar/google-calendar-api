from flask import Flask
from utils import build_service
from googleapiclient.errors import HttpError

app = Flask(__name__)

service = build_service()

calendar_id = "primary"
event_id = "5d81ikjs339u465755iro994kc"

try:
    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    event["summary"] = "Event updated!"

    updated_event = (
        service.events()
        .update(calendarId=calendar_id, eventId=event["id"], body=event)
        .execute()
    )

    # Print the updated date.
    print(updated_event["updated"])
    print("Event updated successfully!")
except HttpError as error:
    print(f"An error occurred: {error}")
    if error.resp.status == 404:
        print("Event not found. Please check the event ID and try again.")

if __name__ == "__main__":
    app.run(debug=True)
