import os
from services.data_service import HSNDataService
from services.validator import HsnValidator
from services.suggester import HsnSuggester
from models.responses import ValidationResponse, SuggestionResponse

class FulfillmentProcessor:
    """ADK fulfillment handler"""

    def __init__(self):
        # Define your GCS path here
        gcs_path = 'hsn-data-bucket/HSN_SAC.xlsx'

        # Initialize HSNDataService with the GCS path
        self.data_service = HSNDataService(gcs_path)

        # Set up validator and suggester using loaded data
        self.validator = HsnValidator(self.data_service)
        self.suggester = HsnSuggester(self.data_service)

    def process(self, intent: str, params: dict) -> dict:
        """ADK fulfillment routing"""
        if intent == 'validate_hsn':
            return self._handle_validation(params)
        elif intent == 'suggest_hsn':
            return self._handle_suggestion(params)
        else:
            return {'fulfillmentText': 'Unsupported intent'}

    def _handle_validation(self, params: dict) -> dict:
        codes = params.get('hsn_code', [])
        if not codes:
            return ValidationResponse.error('No HSN code provided')

        if len(codes) == 1:
            result = self.validator.validate(codes[0])
            return ValidationResponse.from_result(result)
        else:
            results = [self.validator.validate(code) for code in codes]
            return ValidationResponse.bulk_result(results)

    def _handle_suggestion(self, params: dict) -> dict:
        query = params.get('product_description', '')
        if not query:
            return SuggestionResponse.error('No product description provided')

        results = self.suggester.suggest(query)
        return SuggestionResponse.from_results(query, results)
