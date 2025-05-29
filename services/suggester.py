from typing import List, Dict

class HsnSuggester:
    def __init__(self, data_service):
        self.data = data_service

    def suggest(self, query: str) -> List[Dict[str, str]]:
        """Suggest HSN codes based on product description"""
        return self.data.search(query)