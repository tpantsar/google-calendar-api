import os

from dotenv import load_dotenv


class ENVIRONMENT:
    """Environment variables class"""

    def __init__(self):
        project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
        dotenv_path = os.path.join(project_dir, ".env")
        load_dotenv(dotenv_path)
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

    def get_instance(self):
        if not hasattr(self, "_instance"):
            self._instance = ENVIRONMENT()
        return self._instance

    def getClientId(self):
        return self.client_id

    def getClientSecret(self):
        return self.client_secret


CLIENT_ID = ENVIRONMENT().get_instance().getClientId()
CLIENT_SECRET = ENVIRONMENT().get_instance().getClientSecret()
