from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os.path

app = FastAPI()

# CORS middleware to allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load client secrets from credentials.json
CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Configure the OAuth2 flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/auth/google/callback'
)

@app.get('/auth/google')
def auth_google():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return {"auth_url": authorization_url}

@app.get('/auth/google/callback')
def auth_callback(code: str):
    flow.fetch_token(code=code)
    creds = flow.credentials
    # TODO : Save the credentials to the database
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    return {"message": "Authentication successful!"}

@app.get('/api/files')
def list_files():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    return results.get('files', [])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)