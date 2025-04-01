"""Conditions module for evaluating expressions.

This module provides components for defining, validating, and evaluating conditions.
"""
# Import original components for backward compatibility
from src.core.conditions.condition_interface import ConditionInterface, ConditionResult, BooleanCondition
from src.core.conditions.base_condition import BaseCondition as LegacyBaseCondition
from src.core.conditions.operators import create_and_condition, create_or_condition, create_not_condition
from src.core.conditions.composite_conditions import AndCondition as LegacyAndCondition, OrCondition as LegacyOrCondition, NotCondition as LegacyNotCondition
from src.core.conditions.comparison_condition import ComparisonCondition, ComparisonOperator
from src.core.conditions.element_exists_condition import ElementExistsCondition
from src.core.conditions.text_contains_condition import TextContainsCondition
from src.core.conditions.condition_factory import ConditionFactory as LegacyConditionFactory

# Import new interfaces
from .interfaces import (
    ICondition, ICompoundCondition, IConditionFactory,
    IConditionProvider, IConditionRegistry, IConditionResolver
)

# Import new exceptions
from .exceptions import (
    ConditionError, ConditionNotFoundError, ConditionTypeNotFoundError,
    ConditionValidationError, ConditionEvaluationError, ConditionProviderError,
    ConditionRegistryError, ConditionResolverError, ConditionFactoryError
)

# Import new implementations
from .base_condition_new import BaseCondition
from .compound_condition_base import CompoundCondition
from .compound_conditions import AndCondition, OrCondition, NotCondition
from .condition_provider import BaseConditionProvider
from .condition_registry import ConditionRegistry
from .condition_resolver import ConditionResolver
from .condition_factory_new import ConditionFactory
from .standard_provider import StandardConditionProvider
from .standard_conditions import TrueCondition, FalseCondition
from .variable_provider import VariableConditionProvider
from .variable_conditions import (
    VariableCompareCondition, VariableExistsCondition,
    VariableEmptyCondition, VariableTypeCondition
)

__all__ = [
    # Legacy interfaces
    'ConditionInterface',
    'ConditionResult',
    'BooleanCondition',

    # Legacy base classes
    'LegacyBaseCondition',

    # Legacy operators
    'create_and_condition',
    'create_or_condition',
    'create_not_condition',

    # Legacy implementations
    'LegacyAndCondition',
    'LegacyOrCondition',
    'LegacyNotCondition',
    'ComparisonCondition',
    'ComparisonOperator',
    'ElementExistsCondition',
    'TextContainsCondition',

    # Legacy factory
    'LegacyConditionFactory',

    # New interfaces
    'ICondition', 'ICompoundCondition', 'IConditionFactory',
    'IConditionProvider', 'IConditionRegistry', 'IConditionResolver',

    # New exceptions
    'ConditionError', 'ConditionNotFoundError', 'ConditionTypeNotFoundError',
    'ConditionValidationError', 'ConditionEvaluationError', 'ConditionProviderError',
    'ConditionRegistryError', 'ConditionResolverError', 'ConditionFactoryError',

    # New base classes
    'BaseCondition',

    # New compound conditions
    'CompoundCondition', 'AndCondition', 'OrCondition', 'NotCondition',

    # New provider components
    'BaseConditionProvider', 'ConditionRegistry', 'ConditionResolver',

    # New factory
    'ConditionFactory',

    # Standard conditions
    'StandardConditionProvider', 'TrueCondition', 'FalseCondition',

    # Variable conditions
    'VariableConditionProvider', 'VariableCompareCondition',
    'VariableExistsCondition', 'VariableEmptyCondition', 'VariableTypeCondition'
]
