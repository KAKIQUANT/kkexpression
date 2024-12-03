import pandas as pd

def industry_neutralize(factor_data: pd.DataFrame, 
                       industry_data: pd.DataFrame) -> pd.DataFrame:
    """
    Neutralize factor values by industry.
    
    Args:
        factor_data: Factor values DataFrame
        industry_data: Industry classification DataFrame
        
    Returns:
        Industry neutralized factor values
    """
    def neutralize(group):
        return group - group.mean()
        
    return factor_data.groupby(industry_data).apply(neutralize) 