import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Timezone of the calendar, default is Europe/Helsinki (+2 GMT)
TIMEZONE = os.getenv('TZ', 'Europe/Helsinki')

MASON = 'application/vnd.mason+json'
JSON = 'application/json'

ERROR_PROFILE = '/profiles/error/'

TIME_FORMAT_PROMPT = '%Y-%m-%d %H:%M'
TIME_FORMAT_CONSOLE = '%d.%m.%Y %H.%M'
