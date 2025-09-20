from flask import Blueprint, request, jsonify
from routes import require_auth
from services.db_proxy import DatabaseProxy
from services.storage import upload_bytes_and_get_path
from services.analysis import process_in_background

upload_bp = Blueprint("upload", __name__)

@upload_bp.post("/upload")
@require_auth
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Missing file"}), 400
    allowed = (".vcf", ".ab1")
    name = file.filename or "dna"
    if not name.lower().endswith(allowed):
        return jsonify({"error": "Only VCF/AB1 supported"}), 400

    user = request.user
    data = file.read()
    storage_path = upload_bytes_and_get_path(user["uid"], name, data)

    dbx = DatabaseProxy(user)
    file_id = dbx.create_dna_file(name, len(data), storage_path)
    report_id = dbx.upsert_report(None, file_id, "processing", {"riskLevel": None, "score": None})

    process_in_background(user, file_id, report_id, storage_path)
    return jsonify({"report_id": report_id, "message": "File received. Analysis started."})