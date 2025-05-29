from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class HsnCode:
    code: str
    description: str
    parent_code: Optional[str] = None

@dataclass 
class ValidationResult:
    is_valid: bool
    code: str
    description: Optional[str] = None
    error: Optional[str] = None
    hierarchy: Optional[List[Dict[str, str]]] = None

@dataclass
class SuggestionResult:
    query: str
    matches: List[Dict[str, str]]