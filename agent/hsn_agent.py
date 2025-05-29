from google.cloud import dialogflow_v2beta1 as dialogflow
from abc import ABC, abstractmethod
import os

class AbstractAgent(ABC):
    """Base agent class following ADK patterns"""
    
    @abstractmethod
    def handle_request(self, request: dict) -> dict:
        pass

class HsnAgent(AbstractAgent):
    def __init__(self):
        self.session_client = dialogflow.SessionsClient()
        self.project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        
    def detect_intent_text(self, session_id: str, text: str, language_code='en'):
        """ADK-style intent detection"""
        session = self.session_client.session_path(self.project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        
        return self.session_client.detect_intent(
            session=session,
            query_input=query_input
        )
    
    def handle_request(self, request: dict) -> dict:
        """Main request handler following ADK pattern"""
        session_id = request.get('session_id', 'default_session')
        query = request.get('query', '')
        
        intent_response = self.detect_intent_text(session_id, query)
        intent = intent_response.query_result.intent.display_name
        params = intent_response.query_result.parameters
        
        from agent.fulfillment import FulfillmentProcessor
        return FulfillmentProcessor().process(intent, params)