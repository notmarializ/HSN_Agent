from typing import Dict, Any
from models.hsn_code import HsnCode

class HsnValidator:
    def __init__(self, data_service):
        self.data = data_service

    def validate(self, code: str) -> Dict[str, Any]:
        """Validate an HSN code"""
        # Format validation
        if not code.isdigit():
            return {
                'valid': False,
                'code': code,
                'error': 'HSN code must contain only digits'
            }
        
        if len(code) < 2 or len(code) > 8:
            return {
                'valid': False,
                'code': code,
                'error': 'HSN code must be 2-8 digits long'
            }
        
        # Existence validation
        hsn = self.data.get(code)
        if not hsn:
            return {
                'valid': False,
                'code': code,
                'error': 'HSN code not found in database'
            }
        
        # Hierarchy validation
        parents = self.data.get_parents(code)
        
        return {
            'valid': True,
            'code': code,
            'description': hsn.description,
            'hierarchy': parents
        }

    def get_by_code(self, code: str) -> Any:
        """Added for health check or direct access"""
        return self.data.get(code)
    
    def get_parents(self, code: str) -> list:
        """Dummy parent lookup based on code length"""
        if len(code) > 2:
            return [code[:2]]
        return []
