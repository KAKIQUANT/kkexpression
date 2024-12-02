from abc import ABC, abstractmethod
from typing import List, Tuple


class AlphaBase(ABC):
    """Base class for alpha factor implementations."""
    
    def get_label(self) -> Tuple[str, str]:
        """Get label field and name."""
        return "shift(close, -20)/close - 1", 'label'

    @abstractmethod
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        """
        Get factor fields and names.
        
        Returns:
            Tuple of (fields list, names list)
        """
        pass

    def get_field_by_name(self, name: str) -> str:
        """Get field expression by factor name."""
        fields, names = self.get_fields_names()
        for f, n in zip(fields, names):
            if n == name:
                return f
        return None

    def get_ic_labels(self) -> Tuple[List[str], List[str]]:
        """Get IC calculation labels."""
        days = [1, 5, 10, 20]
        fields = [f'shift(close, -{d})/close - 1' for d in days]
        names = [f'return_{d}' for d in days]
        return fields, names

    def get_all_features_names(self) -> Tuple[List[str], List[str]]:
        """Get all factor fields and names including label."""
        fields, names = self.get_fields_names()
        label_field, label_name = self.get_label()

        all_fields = fields.copy()
        all_fields.append(label_field)

        all_names = names.copy()
        all_names.append(label_name)
        return all_fields, all_names


class AlphaLit(AlphaBase):

    def get_fields_names(self):
        fields = []
        names = []

        windows = [2, 5, 10, 20]
        fields += ['close/shift(close,%d) - 1' % d for d in windows]
        names += ['roc_%d' % d for d in windows]

        fields += ['avg(volume,1)/avg(volume,5)']
        names += ['avg_amount_1_avg_amount_5']

        fields += ['avg(volume,5)/avg(volume,20)']
        names += ['avg_amount_5_avg_amount_20']

        fields += ['rank(avg(volume,1))/rank(avg(volume,5))']
        names += ['rank_avg_amount_1_avg_amount_5']

        fields += ['avg(volume,5)/avg(volume,20)']
        names += ['rank_avg_amount_5_avg_amount_20']

        windows = [2, 5, 10]
        fields += ['rank(roc_%d)' % d for d in windows]
        names += ['rank_roc_%d' % d for d in windows]

        fields += ['rank(roc_2)/rank(roc_5)']
        names += ['rank_roc_2_rank_roc_5']

        fields += ['rank(roc_5)/rank(roc_10)']
        names += ['rank_roc_5_rank_roc_10']

        return fields, names

    def get_label(self):
        return "qcut(shift(close, -1)/close - 1,3)", 'label'
