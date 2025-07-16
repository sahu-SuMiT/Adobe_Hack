"""
Base class for PDF outline extractors.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class OutlineExtractorBase(ABC):
    """Base class for PDF outline extractors."""
    
    @abstractmethod
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline from a PDF file."""
        pass 