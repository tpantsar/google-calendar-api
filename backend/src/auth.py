""" Authorize the user to Google Calendar API. """

import os

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from constants import SCOPES
from logger_config import logger


def get_credentials() -> Credentials:
    """
    Get the user credentials for the Google Calendar API.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        logger.debug("Credentials loaded from token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.error("Credentials expired, refreshing")
            logger.debug(f"Credentials: {creds}")
            try:
                creds.refresh(Request())
            except RefreshError as e:
                logger.error(f"Token has been expired or revoked. {e}")
                logger.info("Guiding user to authenticate again.")
                creds = auth_flow()
        else:
            creds = auth_flow()
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            logger.debug("Credentials written to token.json")

    logger.debug("Credentials fetched successfully")
    return creds


def auth_flow() -> Credentials:
    """
    Run the authorization flow for the user to access Google Calendar API.
    """
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    if creds and creds.valid:
        logger.info("Authorization flow completed")
        return creds
    else:
        logger.error("Authorization flow failed")
        return None
