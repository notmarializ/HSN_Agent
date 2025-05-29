import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from agent.webhook_handler import handle_webhook
from services.data_service import HSNDataService
from services.validator import HsnValidator
from services.suggester import HsnSuggester
from typing import Dict, Any

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Config
GCS_HSN_PATH = os.getenv('GCS_HSN_PATH', 'hsn-data-bucket/HSN_SAC.xlsx')
CREDENTIALS_PATH = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS',
    r"C:\Users\lizma\Downloads\hsn-code-agent-461214-6108fd036969.json"
)
SHEET_NAME = os.getenv('SHEET_NAME', 'HSN_MSTR')


def configure_services() -> Dict[str, Any]:
    """Initialize and return all core services"""
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_PATH}")
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH

    try:
        data_service = HSNDataService(GCS_HSN_PATH, sheet_name=SHEET_NAME)
        return {
            'validator': HsnValidator(data_service),
            'suggester': HsnSuggester(data_service),
            'data_service': data_service
        }
    except Exception as e:
        app.logger.error(f"Service initialization failed: {str(e)}")
        raise


def create_app():
    try:
        services = configure_services()
    except Exception as e:
        @app.route('/')
        def service_error():
            return jsonify({"error": f"Service initialization failed: {str(e)}"}), 500
        return app

    @app.route('/')
    def home():
        return jsonify({
            "service": "HSN Code Agent",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "webhook": "/webhook (POST)"
            }
        })

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            req = request.get_json(force=True)
            print("🔹 Incoming request:", req)
            result = handle_webhook(req, services['validator'], services['suggester'])
            print("🔸 Outgoing response:", result)
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Webhook error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/health')
    def health_check():
        try:
            sample_code = next(iter(services['data_service'].code_index.keys()))
            desc = services['data_service'].get_by_code(sample_code)
            return jsonify({"status": "healthy", "sample_code": sample_code, "description": desc}), 200
        except Exception as e:
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
