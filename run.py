from app import create_app
from flask_cors import CORS
import os

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usará su puerto asignado
    app.run(debug=False, host="0.0.0.0", port=port)


