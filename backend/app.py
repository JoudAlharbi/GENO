import os
from flask import Flask, send_from_directory, abort
from config import Config
import firebase_admin
from firebase_admin import credentials

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # فعّلي الاعتماديات قبل أي استيرادات تعتمد عليها
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.FIREBASE_CREDENTIALS
    if not firebase_admin._apps:
        cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred, {"storageBucket": Config.FIREBASE_STORAGE_BUCKET})

    # ← بعد التهيئة، استوردي البلوبربنتس
    from routes.auth import auth_bp
    from routes.upload import upload_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/api")

    @app.get("/dev/files/<path:filepath>")
    def dev_files(filepath):
        safe_root = os.path.abspath(os.getcwd())
        abs_path = os.path.abspath(os.path.join(safe_root, filepath))
        if not abs_path.startswith(safe_root): return abort(403)
        if not os.path.exists(abs_path): return abort(404)
        directory, filename = os.path.split(abs_path)
        return send_from_directory(directory, filename, as_attachment=True)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)