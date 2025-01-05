from services.event import get_popular_events

events = get_popular_events(
    "d0b6f89a41f325b2a45252ce38c35c5885113ec47fc9ee1c3248c83a5898743b@group.calendar.google.com"
)
print(events)

for summary in events:
    print(summary)
