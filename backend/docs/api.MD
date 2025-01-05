## Response Codes:

200 OK: Indicates that the request has succeeded and the resource has been updated. The response body typically contains the updated resource.
204 No Content: Indicates that the request has succeeded and the resource has been updated, but there is no content to send in the response body.

## Endpoints:

- GET /api/events/<calendar_id>
- POST /api/events/<calendar_id>
- PUT /api/events/<calendar_id>/<event_id>
- DELETE /api/events/<calendar_id>/<event_id>
- GET /api/calendars/

## Create event request body:

```json
{
  "start": {
    "dateTime": "2024-11-21T12:00:00+02:00",
    "timeZone": "Europe/Helsinki"
  },
  "end": {
    "dateTime": "2024-11-21T17:00:00+02:00",
    "timeZone": "Europe/Helsinki"
  }
}
```
