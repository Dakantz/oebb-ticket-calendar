import json
import os
from pathlib import Path

CLIENT_SECRET_PATH = Path(os.environ.get("CLIENT_SECRET_FILE", "../client_secret.json"))
_client_secret = json.loads(CLIENT_SECRET_PATH.read_text())["web"]

GOOGLE_CLIENT_ID = _client_secret["client_id"]
GOOGLE_CLIENT_SECRET = _client_secret["client_secret"]
GOOGLE_TOKEN_URI = _client_secret["token_uri"]
GOOGLE_AUTH_URI = _client_secret["auth_uri"]
REDIRECT_URI = _client_secret["redirect_uris"][0]

# default frontend origin: same host as the redirect uri, without the /backend/auth path
FRONTEND_URL = os.environ.get("FRONTEND_URL", REDIRECT_URI.split("/backend/")[0])

SESSION_SECRET = os.environ.get("SESSION_SECRET", "dev-insecure-secret-change-me")

GOOGLE_SCOPES = "openid email https://www.googleapis.com/auth/gmail.readonly"
