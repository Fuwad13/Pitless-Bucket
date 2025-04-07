from config import Config

PB_SETTINGS = "http://localhost:3000/settings"
BACKEND_API_URL = "http://localhost:8000/api/v1"

FIREBASE_CLIENT_CREDS = {
    "type": "service_account",
    "project_id": Config.FIREBASE_PROJECT_ID,
    "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
    "private_key": Config.FIREBASE_PRIVATE_KEY_B64.replace("\\n", "\n"),
    "client_email": Config.FIREBASE_CLIENT_EMAIL,
    "client_id": Config.FIREBASE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": Config.FIREBASE_CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com",
}

HELP_TEXT = """
        Available Commands:
        /start - Show welcome message
        /link - Link to your PitLess Bucket Account
        /unlink - Unlink from your connected PitLess Bucket Account
        /whoami - Check your linked account information.

        /dashboard - Show your Pitless Bucket dashboard         
        /files - List all available files
        /upload - Upload a new file
        /download [filename] Download a file by name
                         
        /help - Show this help message
    """
