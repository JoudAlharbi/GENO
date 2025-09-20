import os, shutil

BASE_UPLOADS = os.path.join("uploads")
BASE_REPORTS = os.path.join("reports")

def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def upload_bytes_and_get_path(user_id: str, filename: str, data: bytes) -> str:
    local_path = os.path.join(BASE_UPLOADS, user_id, filename)
    _ensure_dir(local_path)
    with open(local_path, "wb") as f:
        f.write(data)
    return local_path

def upload_file_and_get_path(user_id: str, local_path: str, dest_name: str) -> str:
    dest_path = os.path.join(BASE_REPORTS, user_id, dest_name)
    _ensure_dir(dest_path)
    shutil.copy(local_path, dest_path)
    return dest_path

def get_signed_url(path: str, minutes: int = 15) -> str:
    return f"/dev/files/{path.replace('\\', '/')}"  # يخدمه app.py محليًا

def delete_blob(path: str):
    try: os.remove(path)
    except FileNotFoundError: pass