from pathlib import Path
from fastapi import Depends
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from db.utils import get_db
from db.models import User, GoogleDrive

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
CLIENT_SECRETS_FILE = Path(__file__).parent / 'credentials.json'
SCOPES = [
    'openid',  # Explicitly request OpenID Connect
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Configure the OAuth2 flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/auth/google/callback',
    # Use these parameters instead of pkce=True
    autogenerate_code_verifier=True,
    code_verifier=None
)

@app.get('/auth/google')
def auth_google():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true'
    )
    return {"auth_url": authorization_url}

@app.get('/auth/google/callback')
def auth_callback(code: str, db: Session = Depends(get_db)):
    print(code)
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open('temp_token.json', 'w') as f:
        f.write(creds.to_json())
    creds = Credentials.from_authorized_user_file('temp_token.json', SCOPES)
    print(creds)
    # Get user info from Google
    service = build('oauth2', 'v2', credentials=creds)
    user_info = service.userinfo().get().execute()
    print(user_info)
    
    # Check if user exists
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        # Create new user
        user = User(
            name=user_info.get('name', 'Unknown'),
            email=user_info['email']
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create GoogleDrive entry
    drive = GoogleDrive(
        user_id=user.id,
        creds=creds.to_json(),
        total_space=15*1024**3  # 15GB in bytes
    )
    db.add(drive)
    db.commit()
    
    return {"message": "Authentication successful!"}

@app.get('/api/files')
def list_files():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    return results.get('files', [])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)