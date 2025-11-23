from src.backend.server import create_app
from dotenv import load_dotenv
import os
import sys
import threading
import webview

load_dotenv()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative)
    return full_path.replace("\\", "/")

def start_flask():
    app = create_app()
    app.run(
        port=8765,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    frontend_index = resource_path("src/frontend/dist/index.html")
    
    webview.create_window("Mi App TODO", frontend_index)
    webview.start()
    
