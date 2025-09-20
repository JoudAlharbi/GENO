from flask import Blueprint, jsonify, request
from routes import require_auth
from services.db_proxy import DatabaseProxy
from services.storage import get_signed_url

reports_bp = Blueprint("reports", __name__)

@reports_bp.get("/report/<report_id>")
@require_auth
def get_report(report_id):
    dbx = DatabaseProxy(request.user)
    doc = dbx.get_report(report_id)
    if not doc:
        return jsonify({"error": "Not found or not authorized"}), 404
    if doc.get("status") != "ready":
        return jsonify({"status": doc.get("status")}), 202
    url = get_signed_url(doc["pdfPath"])
    return jsonify({"download_url": url})

@reports_bp.get("/reports")
@require_auth
def list_reports():
    dbx = DatabaseProxy(request.user)
    items = dbx.list_reports_for_user()
    return jsonify(items)