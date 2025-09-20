from typing import Optional, Dict
from datetime import datetime
from google.cloud import firestore

db = firestore.Client()

class DatabaseProxy:
    def __init__(self, user_claims: dict):
        self.uid = user_claims.get("uid")

    def _owns(self, doc: Dict) -> bool:
        return doc and doc.get("userId") == self.uid

    def create_dna_file(self, filename: str, size: int, storage_path: str) -> str:
        ref = db.collection("dna_files").document()
        ref.set({
            "id": ref.id, "userId": self.uid, "filename": filename,
            "size": size, "storagePath": storage_path,
            "createdAt": datetime.utcnow().isoformat()+"Z", "status": "uploaded"
        })
        return ref.id

    def upsert_report(self, report_id: Optional[str], file_id: str, status: str, payload: Dict):
        ref = db.collection("reports").document(report_id) if report_id else db.collection("reports").document()
        data = {
            "id": ref.id, "userId": self.uid, "fileId": file_id,
            "status": status, **payload, "updatedAt": datetime.utcnow().isoformat()+"Z"
        }
        ref.set(data, merge=True)
        return ref.id

    def list_reports_for_user(self, limit=20):
        q = (db.collection("reports")
             .where("userId", "==", self.uid)
             .order_by("updatedAt", direction=firestore.Query.DESCENDING)
             .limit(limit))
        return [d.to_dict() for d in q.stream()]

    def get_report(self, report_id: str):
        snap = db.collection("reports").document(report_id).get()
        if snap.exists:
            doc = snap.to_dict()
            return doc if self._owns(doc) else None
        return None