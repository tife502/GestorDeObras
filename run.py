from app import create_app
from flask_cors import CORS
import os
from app import create_app, socketio  

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app = create_app()  

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


