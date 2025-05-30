# 🧠 HSN Code Validation and Suggestion Agent

A smart agent that validates and suggests HSN codes based on product descriptions using Flask, Dialogflow, and React. This system is designed to support tax compliance, B2B invoicing, and customs documentation by intelligently guiding users through accurate HSN classification.

---

## 🚀 Features

- ✅ **HSN Code Validation** with format and hierarchy checks
- 🔍 **HSN Code Suggestion** using fuzzy matching for product descriptions
- 💬 **Dialogflow Integration** for natural language interaction
- 🌐 **React Frontend** for local usage and testing
- ⚡ **Real-time Response System** with context-aware responses
- 🧾 Uses `HSN_Master_Data.xlsx` as the core dataset

---

## 🧩 Project Structure

HSN_AGENT/
├── main.py # Entry point for Flask app and webhook
├── app.py # Dialogflow webhook endpoint
├── hsn-frontend/ # Local frontend using React
├── agent/
│ ├── webhook_handler.py # Dialogflow webhook router
│ ├── fulfillment.py # Intent handling logic
│ └── hsn_agent.py # Core agent orchestration
├── services/
│ ├── validator.py # HSN validation logic
│ ├── suggester.py # Fuzzy matching for code suggestions
│ └── data_service.py # Excel data loader and cache
├── models/
│ ├── responses.py # Response format utilities
│ └── hsn_code.py # HSN data model
├── resources/
│ └── HSN_Master_Data.xlsx # Source dataset
├── app.yaml # GCP deployment file for Dialogflow
├── requirements.txt # Python dependency list

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hsn-agent.git
cd hsn-agent
2. Set Up Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Run the Flask App
bash
Copy
Edit
python main.py
4. Start the React Frontend (Optional)
bash
Copy
Edit
cd hsn-frontend
npm install
npm start
🧠 Dialogflow Integration
This system connects with Dialogflow to power conversational HSN code validation and suggestion.

▶️ Run app.py Locally (for Development)
bash
Copy
Edit
python app.py
This will start a Flask server at http://localhost:5000.

Use ngrok to expose it for Dialogflow:

bash
Copy
Edit
ngrok http 5000
Paste the HTTPS URL from ngrok (e.g., https://abcd1234.ngrok.io) into Dialogflow → Fulfillment → Webhook URL.

☁️ Deploy to Google Cloud (Production)
This project is configured for GCP App Engine.

Steps:
Authenticate:

bash
Copy
Edit
gcloud auth login
Set project:

bash
Copy
Edit
gcloud config set project [PROJECT_ID]
Deploy:

bash
Copy
Edit
gcloud app deploy app.yaml
Copy the endpoint URL and use it in your Dialogflow webhook configuration.

📊 Core Functionality Overview
Functionality	Input	Logic Applied	Output
HSN Validation	Raw HSN Code	Format check, hierarchy validation	Valid/Invalid response
Code Suggestion	Product Description	Fuzzy string matching on Excel data	Suggested HSN code list
Agent Integration	Natural Language Query	Intent matching, fulfillment handling	Contextual text response

📸 Output Screenshots
Make sure to add the images under a /screenshots folder

Description	Screenshot
HSN Validation UI	
Code Suggestion UI	
Chat Agent Response	

📂 Data Source
The reference data for validation and suggestion is sourced from:

Copy
Edit
resources/HSN_Master_Data.xlsx
Ensure it's updated periodically based on GST Council notifications or tax authority sources.

🔮 Future Enhancements
🤖 ML-based classification and semantic search

🔄 Live HSN dataset updates from official APIs

🌍 Multi-language support for user queries

🖥️ UI dashboard for business analysts

🔗 ERP integrations (e.g., SAP, Zoho, Tally)

🤝 Contributions
Want to improve the project? You're welcome!

Fork the repo

Create your branch

Submit a PR

Raise issues if you find bugs or want new features

📄 License
This project is licensed under the MIT License.

📬 Contact
Project Maintainer: [your-email@example.com]
Feel free to reach out for feedback, contributions, or integration support.
