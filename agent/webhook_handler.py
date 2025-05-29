from models.responses import ValidationResponse, SuggestionResponse

def handle_webhook(req, validator, suggester):
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')
    print(f"[DEBUG] Received intent: {intent}")  # Optional debug print

    if intent == 'ValidateHSNCode':
        hsn_code = req['queryResult']['parameters'].get('hsn_code')
        result = validator.validate(hsn_code)
        is_valid = result.get('valid', False)

        formatted_result = {
            'valid': is_valid,
            'code': hsn_code,
            **result
        }
        return ValidationResponse.from_result(formatted_result)

    elif intent == 'SuggestHSNCode':
        description = req['queryResult']['parameters'].get('description')
        suggestions = suggester.suggest(description)

        formatted_results = [{
            'code': sug['code'],
            'description': sug['description'],
            'confidence': sug['confidence']
        } for sug in suggestions]

        return SuggestionResponse.from_results(description, formatted_results)

    # --- New SAC intents ---

    elif intent == 'ValidateSACCode':
        sac_code = req['queryResult']['parameters'].get('sac_code')
        result = validator.validate_sac(sac_code)
        is_valid = result.get('valid', False)

        formatted_result = {
            'valid': is_valid,
            'code': sac_code,
            **result
        }
        return ValidationResponse.from_result(formatted_result)

    elif intent == 'SuggestSACCode':
        description = req['queryResult']['parameters'].get('description')
        suggestions = suggester.suggest_sac(description)

        formatted_results = [{
            'code': sug['code'],
            'description': sug['description'],
            'confidence': sug['confidence']
        } for sug in suggestions]

        return SuggestionResponse.from_results(description, formatted_results)

    return ValidationResponse.error("Unsupported intent")
