""" Authorize the user to Google Calendar API. """

import os
import socket
from contextlib import closing

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.constants import SCOPES
from src.logger_config import logger
from src.printer import Printer


def get_credentials() -> Credentials:
    """
    Get the user credentials for the Google Calendar API (OAuth 2.0).
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    creds = None
    if os.path.exists("creds/token.json"):
        creds = Credentials.from_authorized_user_file("creds/token.json", SCOPES)
        logger.debug("Credentials loaded from token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.error("Credentials expired, refreshing")
            logger.debug("Credentials: %s", creds)
            try:
                creds.refresh(Request())
            except RefreshError as e:
                logger.error("Token has been expired or revoked. %s", e)
                logger.info("Guiding user to authenticate again.")
                creds = auth_flow()
        else:
            creds = auth_flow()
        with open("creds/token.json", "w") as token:
            token.write(creds.to_json())
            logger.debug("Credentials written to token.json")

    logger.debug("Credentials fetched successfully")
    return creds


def authenticate(
    client_id: str, client_secret: str, printer: Printer, local: bool
) -> Credentials:
    flow = InstalledAppFlow.from_client_config(
        client_config={
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=SCOPES,
    )
    if not local:
        printer.msg(
            "Note: Behavior of the `--noauth-local-server` option has changed! "
            "Starting local server, but providing instructions for connecting "
            "to it remotely...\n"
        )
    credentials = None
    attempt_num = 0
    # Retry up to 5 attempts with different random ports.
    while credentials is None:
        port = _free_local_port()
        if not local:
            printer.msg("Option 1 (outbound):\n", "yellow")
            printer.msg(
                "  To establish a connection from this system to a remote "
                "host, execute a command like: `ssh username@host -L "
                f"{port}:localhost:{port} BROWSER=open $BROWSER "
                "'https://the-url-below'`\n",
            )
            printer.msg("Option 2 (outbound):\n", "yellow")
            printer.msg(
                "  To establish a connection from a remote host to this "
                "system, execute a command from remote host like: "
                f"`ssh username@host -fN -R {port}:localhost:{port} ; "
                "BROWSER=open $BROWSER https://the-url-below'`\n\n",
            )
        try:
            credentials = flow.run_local_server(open_browser=False, port=port)
        except OSError as e:
            if e.errno == 98 and attempt_num < 4:
                # Will get retried with a different port.
                printer.msg(f"Port {port} in use, trying another port...")
                attempt_num += 1
            else:
                raise
        except RecursionError:
            raise OSError(
                "Failed to fetch credentials. If this is a nonstandard gcalcli "
                "install, please try again with a system-installed gcalcli as "
                "a workaround.\n"
                "Details: https://github.com/insanum/gcalcli/issues/735."
            )
    return credentials


def _free_local_port():
    # See https://stackoverflow.com/a/45690594.
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def auth_flow() -> Credentials:
    """
    Run the authorization flow for the user to access Google Calendar API.
    """
    logger.debug("Running the authorization flow")
    flow = InstalledAppFlow.from_client_secrets_file("creds/credentials.json", SCOPES)
    creds = flow.run_local_server(open_browser=False, port=0)
    if creds and creds.valid:
        logger.info("Authorization flow completed")
        return creds
    else:
        logger.error("Authorization flow failed")
        return None
