"""
============================================
RUN.PY — Start the Backend Server
============================================

Usage:
    cd backend
    python run.py
"""

from api.app import create_app
import config

app = create_app()

if __name__ == "__main__":
    print("")
    print("=" * 55)
    print("🛡️   SafeClick  — Phishing Detection API")
    print("=" * 55)
    print(f"📡 Server:    http://localhost:{config.SERVER_PORT}")
    print(f"📡 Scan URL:  http://localhost:{config.SERVER_PORT}/api/scan")
    print(f"📡 Health:    http://localhost:{config.SERVER_PORT}/api/health")
    print(f"🔧 Debug:     {config.DEBUG_MODE}")
    print("=" * 55)
    print("Press CTRL+C to stop the server")
    print("")

    app.run(
        debug=config.DEBUG_MODE,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
    )