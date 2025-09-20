import os
USE_LOCAL = os.getenv("USE_LOCAL_STORAGE", "false").lower() == "true"

if USE_LOCAL:
    from services.storage_local import (
        upload_bytes_and_get_path,
        upload_file_and_get_path,
        get_signed_url,
        delete_blob,
    )
else:
    import datetime
    from google.cloud import storage
    from flask import current_app

    def _bucket():
        client = storage.Client()
        return client.bucket(current_app.config["FIREBASE_STORAGE_BUCKET"])

    def upload_bytes_and_get_path(user_id: str, filename: str, data: bytes) -> str:
        blob_path = f"users/{user_id}/uploads/{filename}"
        blob = _bucket().blob(blob_path)
        blob.upload_from_string(data)
        return blob_path

    def upload_file_and_get_path(user_id: str, local_path: str, dest_name: str) -> str:
        blob_path = f"users/{user_id}/reports/{dest_name}"
        blob = _bucket().blob(blob_path)
        blob.upload_from_filename(local_path)
        return blob_path

    def get_signed_url(blob_path: str, minutes: int = 15) -> str:
        blob = _bucket().blob(blob_path)
        return blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=minutes),
            method="GET",
        )

    def delete_blob(blob_path: str):
        _bucket().blob(blob_path).delete(timeout=30)