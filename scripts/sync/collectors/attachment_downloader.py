"""Attachment downloader with caching support."""

import base64
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Add root for lib imports
sys.path.insert(0, str(Path(__file__).parents[4]))

from lib.gmail import GmailClient

sys.path.insert(0, str(Path(__file__).parents[1]))
from models_v2 import Attachment


class AttachmentDownloader:
    """Download and cache email attachments."""

    CACHE_INDEX_FILE = ".attachment_cache.json"

    def __init__(
        self,
        gmail_client: Optional[GmailClient] = None,
        cache_dir: Optional[Path] = None,
    ):
        """
        Initialize downloader.

        Args:
            gmail_client: Gmail API client
            cache_dir: Directory to store downloaded files
        """
        self.gmail_client = gmail_client or GmailClient()
        self.cache_dir = cache_dir or Path("./attachments")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_index = self._load_cache_index()

    def _load_cache_index(self) -> dict:
        """Load cache index from disk."""
        index_path = self.cache_dir / self.CACHE_INDEX_FILE
        if index_path.exists():
            try:
                return json.loads(index_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"version": "1.0", "files": {}}

    def _save_cache_index(self):
        """Save cache index to disk."""
        index_path = self.cache_dir / self.CACHE_INDEX_FILE
        index_path.write_text(
            json.dumps(self._cache_index, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _get_cache_key(self, email_id: str, attachment_id: str) -> str:
        """Generate cache key from email and attachment IDs."""
        return hashlib.md5(f"{email_id}:{attachment_id}".encode()).hexdigest()[:16]

    def _get_cached_path(self, email_id: str, attachment_id: str) -> Optional[Path]:
        """Get cached file path if exists."""
        cache_key = self._get_cache_key(email_id, attachment_id)
        if cache_key in self._cache_index.get("files", {}):
            cached = self._cache_index["files"][cache_key]
            path = Path(cached["path"])
            if path.exists():
                return path
        return None

    def download(
        self,
        email_id: str,
        attachment_id: str,
        filename: Optional[str] = None,
    ) -> Path:
        """
        Download a single attachment.

        Args:
            email_id: Gmail message ID
            attachment_id: Attachment ID
            filename: Optional filename (uses attachment filename if not provided)

        Returns:
            Path to downloaded file
        """
        # Check cache first
        cached = self._get_cached_path(email_id, attachment_id)
        if cached:
            return cached

        # Download via Gmail API
        service = self.gmail_client.service
        attachment = service.users().messages().attachments().get(
            userId="me",
            messageId=email_id,
            id=attachment_id,
        ).execute()

        data = attachment.get("data", "")
        file_data = base64.urlsafe_b64decode(data)

        # Generate safe filename
        if not filename:
            filename = f"attachment_{email_id[:8]}_{attachment_id[:8]}"

        # Sanitize filename
        safe_filename = "".join(
            c for c in filename if c.isalnum() or c in "._- "
        ).strip()
        if not safe_filename:
            safe_filename = f"file_{attachment_id[:12]}"

        # Add date prefix for organization
        date_prefix = datetime.now().strftime("%Y%m%d")
        output_path = self.cache_dir / f"{date_prefix}_{safe_filename}"

        # Handle duplicates
        counter = 1
        base_path = output_path
        while output_path.exists():
            stem = base_path.stem
            suffix = base_path.suffix
            output_path = base_path.with_name(f"{stem}_{counter}{suffix}")
            counter += 1

        # Write file
        output_path.write_bytes(file_data)

        # Update cache index
        cache_key = self._get_cache_key(email_id, attachment_id)
        self._cache_index["files"][cache_key] = {
            "email_id": email_id,
            "attachment_id": attachment_id,
            "filename": filename,
            "path": str(output_path),
            "size": len(file_data),
            "downloaded_at": datetime.now().isoformat(),
        }
        self._save_cache_index()

        return output_path

    def download_all(self, email_id: str) -> List[Attachment]:
        """
        Download all attachments from an email.

        Args:
            email_id: Gmail message ID

        Returns:
            List of Attachment objects with local_path set
        """
        # Get email with attachments
        email = self.gmail_client.get_email(email_id)

        results = []
        for att in email.attachments:
            try:
                local_path = self.download(
                    email_id=email_id,
                    attachment_id=att.id,
                    filename=att.filename,
                )

                results.append(Attachment(
                    id=att.id,
                    email_id=email_id,
                    filename=att.filename,
                    mime_type=att.mime_type,
                    size=att.size,
                    local_path=str(local_path),
                    parsed=False,
                ))
            except Exception as e:
                print(f"Error downloading {att.filename}: {e}")
                # Still add to results without local_path
                results.append(Attachment(
                    id=att.id,
                    email_id=email_id,
                    filename=att.filename,
                    mime_type=att.mime_type,
                    size=att.size,
                    parsed=False,
                ))

        return results

    def get_quote_attachments(self, email_id: str) -> List[Attachment]:
        """
        Download only quote-related attachments (PDF, Excel).

        Args:
            email_id: Gmail message ID

        Returns:
            List of quote-related Attachment objects
        """
        all_attachments = self.download_all(email_id)

        return [
            att for att in all_attachments
            if att.file_type in ["pdf", "excel"] or att.is_quote_file
        ]

    def clear_cache(self, older_than_days: int = 30):
        """
        Clear cached files older than specified days.

        Args:
            older_than_days: Remove files older than this many days
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=older_than_days)
        files_to_remove = []

        for cache_key, info in list(self._cache_index.get("files", {}).items()):
            downloaded_at = datetime.fromisoformat(info.get("downloaded_at", "2000-01-01"))
            if downloaded_at < cutoff:
                files_to_remove.append(cache_key)
                path = Path(info.get("path", ""))
                if path.exists():
                    try:
                        path.unlink()
                    except Exception:
                        pass

        for key in files_to_remove:
            del self._cache_index["files"][key]

        self._save_cache_index()
        print(f"Cleared {len(files_to_remove)} cached files")
