from typing import List, Tuple
from abc import ABC, abstractmethod


class AlphaBase(ABC):
    """Base class for alpha factor implementations."""
    
    @abstractmethod
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        """
        Get factor fields and names.
        
        Returns:
            Tuple containing:
            - List of factor names
            - List of factor expressions
        """
        pass
    
    def __str__(self) -> str:
        """Return string representation of the alpha class."""
        return self.__class__.__name__
