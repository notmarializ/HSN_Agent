# models/responses.py

class ValidationResponse:
    @staticmethod
    def from_result(data):
        return {
            "fulfillmentText": f"HSN Code {data['code']} is {'valid ✅' if data['valid'] else 'invalid ❌'}.\n"
                               f"{data.get('description', '')}",
            "payload": data
        }

    @staticmethod
    def error(message):
        return {
            "fulfillmentText": f"❗ Error: {message}",
            "payload": {"error": message}
        }


class SuggestionResponse:
    @staticmethod
    def from_results(query, results):
        if not results:
            return {"fulfillmentText": f"❌ No HSN suggestions found for: '{query}'"}

        suggestions = "\n".join([
            f"{r['code']} — {r['description']} (Confidence: {r['confidence']}%)"
            for r in results
        ])

        return {
            "fulfillmentText": f"🔍 Suggestions for '{query}':\n{suggestions}",
            "payload": results
        }
