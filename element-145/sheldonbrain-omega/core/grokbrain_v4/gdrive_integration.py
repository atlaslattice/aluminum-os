#!/usr/bin/env python3
"""
Grokbrain v4.0 - Google Drive Integration
Download chat exports from shared Google Drive folder
"""

import os
import io
from pathlib import Path
from typing import List, Optional
import structlog

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import pickle
except ImportError:
    logger = structlog.get_logger()
    logger.warning("google_api_not_installed",
                  message="Google Drive integration requires: pip install google-auth google-auth-oauthlib google-api-python-client")

logger = structlog.get_logger()

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_gdrive(credentials_file: str = 'credentials.json', token_file: str = 'token.pickle') -> Optional[object]:
    """
    Authenticate with Google Drive API

    Args:
        credentials_file: Path to OAuth2 credentials JSON (download from Google Cloud Console)
        token_file: Path to save authentication token for reuse

    Returns: Google Drive service object or None
    """
    creds = None

    # Load existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("credentials_refreshed")
        else:
            if not os.path.exists(credentials_file):
                logger.error("credentials_file_missing",
                           file=credentials_file,
                           message="Download OAuth2 credentials from Google Cloud Console")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("new_credentials_created")

        # Save token for reuse
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('drive', 'v3', credentials=creds)
        logger.info("gdrive_authenticated")
        return service
    except Exception as e:
        logger.error("gdrive_auth_failed", error=str(e))
        return None


def download_from_gdrive(
    folder_id: str,
    output_dir: str = './exports',
    file_extensions: List[str] = ['.json'],
    credentials_file: str = 'credentials.json'
) -> int:
    """
    Download all files from Google Drive folder

    Args:
        folder_id: Google Drive folder ID (from URL: https://drive.google.com/drive/folders/FOLDER_ID)
        output_dir: Local directory to save files
        file_extensions: List of file extensions to download (e.g., ['.json', '.txt'])
        credentials_file: Path to OAuth2 credentials

    Returns: Number of files downloaded
    """
    service = authenticate_gdrive(credentials_file)
    if not service:
        logger.error("authentication_required")
        return 0

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    downloaded_count = 0

    try:
        # List files in folder
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="files(id, name, mimeType, size)"
        ).execute()

        files = results.get('files', [])
        logger.info("gdrive_files_found", count=len(files), folder_id=folder_id)

        if not files:
            logger.warning("no_files_in_folder", folder_id=folder_id)
            return 0

        for file in files:
            file_name = file['name']
            file_id = file['id']
            mime_type = file['mimeType']

            # Skip Google Docs/Sheets/Slides
            if mime_type.startswith('application/vnd.google-apps'):
                logger.debug("skipping_google_app", name=file_name, mime=mime_type)
                continue

            # Check file extension
            if file_extensions:
                if not any(file_name.endswith(ext) for ext in file_extensions):
                    logger.debug("skipping_extension", name=file_name)
                    continue

            # Download file
            output_path = os.path.join(output_dir, file_name)

            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(output_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.debug("downloading", file=file_name, progress=f"{progress}%")

            fh.close()
            downloaded_count += 1
            logger.info("file_downloaded", file=file_name, path=output_path)

        logger.info("gdrive_download_complete", total_files=downloaded_count)
        return downloaded_count

    except Exception as e:
        logger.error("gdrive_download_error", error=str(e))
        return downloaded_count


def get_gdrive_folder_id_from_url(url: str) -> Optional[str]:
    """
    Extract folder ID from Google Drive URL

    Examples:
        https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9
        https://drive.google.com/drive/u/0/folders/1a2b3c4d5e6f7g8h9

    Returns: Folder ID or None
    """
    if '/folders/' in url:
        parts = url.split('/folders/')
        if len(parts) > 1:
            folder_id = parts[1].split('?')[0].split('/')[0]
            return folder_id
    return None


def setup_gdrive_instructions():
    """
    Print setup instructions for Google Drive integration
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  GOOGLE DRIVE INTEGRATION SETUP                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

To download chat exports from Google Drive, you need OAuth2 credentials:

1. Go to Google Cloud Console: https://console.cloud.google.com/

2. Create a new project (or use existing):
   - Click "Select a project" → "New Project"
   - Name it "Grokbrain" → Create

3. Enable Google Drive API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

4. Create OAuth2 credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Grokbrain Desktop"
   - Click "Create"

5. Download credentials:
   - Click the download icon next to your OAuth client
   - Save as: credentials.json (in project root)

6. Run the pipeline:
   - First run will open browser for authentication
   - Grant access to read Google Drive files
   - Token saved for future runs

7. Share your Google Drive folder:
   - Right-click folder → Share
   - Change to "Anyone with the link can view"
   - Copy the folder URL

8. Use in pipeline:
   python main.py --gdrive "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"

╔══════════════════════════════════════════════════════════════════════════════╗
║  Security Note: credentials.json and token.pickle contain sensitive data.    ║
║  DO NOT commit to Git. Already added to .gitignore                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
