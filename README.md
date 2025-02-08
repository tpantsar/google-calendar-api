## Docker deployment:

1. Download OAuth 2.0 credentials from Google Cloud Platform
   https://console.cloud.google.com/apis/credentials

2. Place credentials.json in `backend/creds` directory
3. Build and run Docker container

```bash
docker compose up -d --build
```

### Run CLI application:

```bash
docker run --rm -it google-calendar-cli bash -c "python terminal.py"
```

## References:

- [Google Calendar API (Google Cloud)](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com)

- [OAuth 2.0 credentials (Google Cloud)](https://console.cloud.google.com/apis/credentials)

- [Docker Hub](https://hub.docker.com/)
