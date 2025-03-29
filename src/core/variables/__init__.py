"""Variable module for managing variables in workflows"""
from src.core.variables.variable_interface import (
    VariableType, VariableChangeEvent, IVariable, IValueHolder, ITyped, IObservable, ISerializable, IMetadata
)
from src.core.variables.variable import Variable
from src.core.variables.typed_variables import (
    StringVariable, NumberVariable, BooleanVariable, ListVariable, DictionaryVariable
)
from src.core.variables.variable_factory import VariableFactory

__all__ = [
    'VariableType',
    'VariableChangeEvent',
    'IVariable',
    'IValueHolder',
    'ITyped',
    'IObservable',
    'ISerializable',
    'IMetadata',
    'Variable',
    'StringVariable',
    'NumberVariable',
    'BooleanVariable',
    'ListVariable',
    'DictionaryVariable',
    'VariableFactory'
]
