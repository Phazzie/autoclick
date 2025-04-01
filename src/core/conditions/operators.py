"""Operator implementations for conditions."""

def create_and_condition(left, right):
    """
    Create an AND condition.
    
    Args:
        left: Left condition
        right: Right condition
        
    Returns:
        A new AND condition
    """
    # Lazy import to avoid circular dependency
    from src.core.conditions.composite_conditions import AndCondition
    return AndCondition(left, right)

def create_or_condition(left, right):
    """
    Create an OR condition.
    
    Args:
        left: Left condition
        right: Right condition
        
    Returns:
        A new OR condition
    """
    from src.core.conditions.composite_conditions import OrCondition
    return OrCondition(left, right)

def create_not_condition(condition):
    """
    Create a NOT condition.
    
    Args:
        condition: Condition to negate
        
    Returns:
        A new NOT condition
    """
    from src.core.conditions.composite_conditions import NotCondition
    return NotCondition(condition)
