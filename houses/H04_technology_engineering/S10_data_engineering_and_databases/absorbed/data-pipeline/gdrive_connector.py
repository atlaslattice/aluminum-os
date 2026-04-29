#!/usr/bin/env python3
"""
Google Drive Connector
Direct integration with Google Drive API for automated content ingestion

Features:
- OAuth2 authentication
- Folder monitoring
- File type detection and parsing
- Batch processing
- Progress tracking
"""

import os
import io
import mimetypes
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

import structlog
from tqdm import tqdm

logger = structlog.get_logger()

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveConnector:
    """
    Connect to Google Drive and fetch files for ingestion

    Supports:
    - OAuth2 authentication
    - Folder monitoring
    - Multiple file types (Docs, PDFs, text files)
    - Batch processing
    - Incremental fetching (only new files)
    """

    # Supported MIME types
    MIME_TYPES = {
        # Google Workspace types
        'application/vnd.google-apps.document': 'text/plain',  # Google Docs → plain text
        'application/vnd.google-apps.spreadsheet': 'text/csv',  # Sheets → CSV
        'application/vnd.google-apps.presentation': 'text/plain',  # Slides → text

        # Standard types
        'text/plain': None,  # Already text
        'application/pdf': None,  # PDF (requires special handling)
        'text/markdown': None,
        'text/html': None,
    }

    def __init__(self,
                 credentials_file: str = "credentials.json",
                 token_file: str = "token.json",
                 scopes: List[str] = SCOPES):
        """
        Initialize Google Drive connector

        Args:
            credentials_file: Path to OAuth2 credentials JSON
            token_file: Path to store/load access token
            scopes: Google API scopes
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = scopes

        self.service = None
        self.creds = None

        # Connect to Drive API
        self._authenticate()

        logger.info("gdrive_connector_initialized")

    def _authenticate(self):
        """Authenticate with Google Drive API"""
        # Load existing token if available
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        # Refresh or obtain new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("refreshing_gdrive_token")
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Google Drive credentials not found: {self.credentials_file}\n"
                        f"Download from: https://console.cloud.google.com/apis/credentials"
                    )

                logger.info("starting_oauth_flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

            logger.info("gdrive_credentials_saved")

        # Build Drive API service
        self.service = build('drive', 'v3', credentials=self.creds)
        logger.info("gdrive_service_ready")

    def list_files(self,
                   folder_id: Optional[str] = None,
                   mime_types: Optional[List[str]] = None,
                   modified_after: Optional[str] = None,
                   max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List files in Google Drive

        Args:
            folder_id: Folder ID to search in (None = entire Drive)
            mime_types: Filter by MIME types
            modified_after: ISO timestamp to get only recently modified files
            max_results: Maximum number of results

        Returns:
            List of file metadata dicts
        """
        try:
            # Build query
            query_parts = []

            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")

            if mime_types:
                mime_queries = [f"mimeType='{mt}'" for mt in mime_types]
                query_parts.append(f"({' or '.join(mime_queries)})")

            if modified_after:
                query_parts.append(f"modifiedTime > '{modified_after}'")

            # Add: not trashed
            query_parts.append("trashed=false")

            query = " and ".join(query_parts) if query_parts else None

            logger.info("listing_gdrive_files", folder_id=folder_id, query=query)

            # Execute query
            results = self.service.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime, size, webViewLink, owners)"
            ).execute()

            files = results.get('files', [])

            logger.info("gdrive_files_listed", count=len(files))

            return files

        except HttpError as e:
            logger.error("gdrive_list_error", error=str(e))
            raise

    def get_file_content(self, file_id: str, mime_type: str) -> str:
        """
        Get file content as text

        Args:
            file_id: Google Drive file ID
            mime_type: File MIME type

        Returns:
            File content as string
        """
        try:
            # Check if needs conversion
            export_mime = self.MIME_TYPES.get(mime_type)

            if export_mime:
                # Export Google Workspace file
                logger.debug("exporting_gdrive_file", file_id=file_id, export_type=export_mime)
                request = self.service.files().export_media(fileId=file_id, mimeType=export_mime)
            else:
                # Download regular file
                logger.debug("downloading_gdrive_file", file_id=file_id)
                request = self.service.files().get_media(fileId=file_id)

            # Download to memory
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Convert to text
            file_buffer.seek(0)
            content = file_buffer.read().decode('utf-8', errors='ignore')

            logger.debug("gdrive_file_downloaded", file_id=file_id, size=len(content))

            return content

        except HttpError as e:
            logger.error("gdrive_download_error", file_id=file_id, error=str(e))
            return ""

    def fetch_folder(self,
                    folder_id: str,
                    modified_after: Optional[str] = None,
                    max_files: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch all supported files from a folder

        Args:
            folder_id: Google Drive folder ID
            modified_after: Only fetch files modified after this time
            max_files: Maximum files to fetch

        Returns:
            List of file data dicts with content
        """
        logger.info("fetching_gdrive_folder", folder_id=folder_id)

        # Get supported MIME types
        supported_types = list(self.MIME_TYPES.keys())

        # List files
        files = self.list_files(
            folder_id=folder_id,
            mime_types=supported_types,
            modified_after=modified_after,
            max_results=max_files
        )

        if not files:
            logger.info("no_files_found", folder_id=folder_id)
            return []

        # Fetch content for each file
        results = []

        print(f"\n📥 Fetching {len(files)} files from Google Drive...")

        for file_meta in tqdm(files, desc="Downloading"):
            try:
                # Get content
                content = self.get_file_content(file_meta['id'], file_meta['mimeType'])

                if not content:
                    logger.warning("empty_file_skipped", file_id=file_meta['id'])
                    continue

                # Prepare result
                file_data = {
                    "title": file_meta['name'],
                    "content": content,
                    "source": file_meta.get('webViewLink', f"gdrive://{file_meta['id']}"),
                    "source_type": "gdrive",
                    "file_id": file_meta['id'],
                    "mime_type": file_meta['mimeType'],
                    "published_date": file_meta.get('modifiedTime', datetime.now().isoformat()),
                    "size_bytes": file_meta.get('size', 0),
                    "authors": [owner.get('displayName', 'Unknown') for owner in file_meta.get('owners', [])]
                }

                results.append(file_data)

            except Exception as e:
                logger.error("file_fetch_failed",
                           file_id=file_meta['id'],
                           name=file_meta['name'],
                           error=str(e))

        logger.info("gdrive_folder_fetched",
                   folder_id=folder_id,
                   files_fetched=len(results))

        return results

    def watch_folder(self,
                    folder_id: str,
                    callback: callable,
                    poll_interval: int = 300):
        """
        Watch folder for new files (polling-based)

        Args:
            folder_id: Folder to watch
            callback: Function to call with new files
            poll_interval: Seconds between checks

        Note: This is a simple polling implementation
        For production, consider using Google Drive API push notifications
        """
        import time

        logger.info("watching_gdrive_folder", folder_id=folder_id, interval=poll_interval)

        last_check = datetime.now().isoformat()

        while True:
            try:
                # Fetch files modified since last check
                new_files = self.fetch_folder(
                    folder_id=folder_id,
                    modified_after=last_check
                )

                if new_files:
                    logger.info("new_files_detected", count=len(new_files))
                    callback(new_files)

                # Update last check time
                last_check = datetime.now().isoformat()

                # Wait before next check
                time.sleep(poll_interval)

            except KeyboardInterrupt:
                logger.info("watch_stopped")
                break

            except Exception as e:
                logger.error("watch_error", error=str(e))
                time.sleep(poll_interval)

    def get_folder_id_from_url(self, url: str) -> str:
        """
        Extract folder ID from Google Drive URL

        Args:
            url: Google Drive folder URL

        Returns:
            Folder ID

        Example:
            https://drive.google.com/drive/folders/ABC123
            → ABC123
        """
        if '/folders/' in url:
            return url.split('/folders/')[1].split('?')[0]
        else:
            raise ValueError(f"Invalid Google Drive folder URL: {url}")


# CLI interface
def main():
    """CLI for testing Google Drive connector"""
    import argparse
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description="Google Drive Connector")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID")
    parser.add_argument("--max-files", type=int, default=10, help="Max files to fetch")
    parser.add_argument("--credentials", default="credentials.json", help="OAuth2 credentials file")
    parser.add_argument("--output", help="Output JSON file")

    args = parser.parse_args()

    print("=" * 70)
    print("GOOGLE DRIVE CONNECTOR TEST")
    print("=" * 70)
    print()

    try:
        # Initialize connector
        connector = GoogleDriveConnector(credentials_file=args.credentials)

        # Fetch folder
        files = connector.fetch_folder(
            folder_id=args.folder_id,
            max_files=args.max_files
        )

        print()
        print(f"✅ Fetched {len(files)} files")
        print()

        # Display results
        for i, file_data in enumerate(files, 1):
            print(f"{i}. {file_data['title']}")
            print(f"   Source: {file_data['source']}")
            print(f"   Size: {len(file_data['content'])} chars")
            print()

        # Save to file if requested
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(files, f, indent=2)
            print(f"💾 Saved to: {args.output}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
