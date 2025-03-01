from flask import Flask, request, jsonify
from flask_cors import CORS
from api.routes import api_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}) 