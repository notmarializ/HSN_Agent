from flask import Flask, request, jsonify
from services.data_service import HSNDataService   # replace with your actual module path
from services.validator import HsnValidator
from services.suggester import HsnSuggester
from agent.webhook_handler import handle_webhook

app = Flask(__name__)

# Initialize your data service with your GCS path and sheet name
# Replace 'your-bucket/hsn-codes.xlsx' and 'Sheet1' accordingly
data_service = HSNDataService(
    gcs_path='hsn-data-bucket/HSN_SAC.xlsx',
    sheet_name="HSN_MSTR"
)

# Inject the data service into validator and suggester
validator = HsnValidator(data_service)
suggester = HsnSuggester(data_service)

@app.route('/', methods=['GET'])
def index():
    return "✅ HSN Agent is running"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    response = handle_webhook(req, validator, suggester)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
