import os, tempfile, threading
from services.storage import upload_file_and_get_path  # , delete_blob
from services.db_proxy import DatabaseProxy
from services.report_gen import build_pdf
from ai.predict import run_analysis_with_model

def _get_local_or_tmp_copy(path: str) -> str:
    return path  # محليًا الملف موجود مباشرة داخل uploads/

def _worker(user: dict, file_id: str, report_id: str, storage_path: str):
    dbx = DatabaseProxy(user)
    tmp_vcf = _get_local_or_tmp_copy(storage_path)
    results = run_analysis_with_model(tmp_vcf)

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    build_pdf(tmp_pdf, report_id, results)
    pdf_blob = upload_file_and_get_path(user["uid"], tmp_pdf, f"{report_id}.pdf")
    try: os.remove(tmp_pdf)
    except: pass

    dbx.upsert_report(report_id, file_id, "ready", {
        "riskLevel": results["risk_level"],
        "score": results["score"],
        "pdfPath": pdf_blob
    })

def process_in_background(user: dict, file_id: str, report_id: str, storage_path: str):
    threading.Thread(target=_worker, args=(user, file_id, report_id, storage_path), daemon=True).start()