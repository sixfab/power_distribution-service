from src.main import app
import os

if __name__ == "__main__":
    is_debug_enabled = os.getenv("DEBUG")
    app.run(host="0.0.0.0", port=6060, threaded=False, processes=1, debug=bool(is_debug_enabled))
