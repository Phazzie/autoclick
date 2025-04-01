"""
Workflow query implementation.

This module provides implementations of workflow queries,
for filtering workflows in a repository.
"""
from typing import Dict, Any, List, Optional, Set, Callable
import operator
import re

from .service_interfaces import IWorkflowQuery
from .interfaces import IWorkflow
from .service_exceptions import WorkflowQueryError


class WorkflowQuery(IWorkflowQuery):
    """
    Base class for workflow queries.
    
    This class provides a base implementation of the IWorkflowQuery interface,
    with common functionality for all query types.
    """
    
    def __and__(self, other: IWorkflowQuery) -> IWorkflowQuery:
        """
        Combine this query with another using AND logic.
        
        Args:
            other: Another query
            
        Returns:
            A new query that matches workflows matching both queries
        """
        return AndQuery(self, other)
    
    def __or__(self, other: IWorkflowQuery) -> IWorkflowQuery:
        """
        Combine this query with another using OR logic.
        
        Args:
            other: Another query
            
        Returns:
            A new query that matches workflows matching either query
        """
        return OrQuery(self, other)
    
    def __invert__(self) -> IWorkflowQuery:
        """
        Negate this query using NOT logic.
        
        Returns:
            A new query that matches workflows not matching this query
        """
        return NotQuery(self)


class PropertyQuery(WorkflowQuery):
    """
    Query that filters workflows based on a property value.
    
    This class provides a query that filters workflows based on a property value,
    using a comparison operator.
    """
    
    # Supported operators
    OPERATORS = {
        'eq': operator.eq,
        'ne': operator.ne,
        'lt': operator.lt,
        'le': operator.le,
        'gt': operator.gt,
        'ge': operator.ge,
        'in': lambda x, y: x in y,
        'not_in': lambda x, y: x not in y,
        'contains': lambda x, y: y in x if isinstance(x, (str, list, tuple, set)) else False,
        'not_contains': lambda x, y: y not in x if isinstance(x, (str, list, tuple, set)) else True,
        'starts_with': lambda x, y: x.startswith(y) if isinstance(x, str) else False,
        'ends_with': lambda x, y: x.endswith(y) if isinstance(x, str) else False,
        'matches': lambda x, y: bool(re.search(y, x)) if isinstance(x, str) else False
    }
    
    def __init__(self, property_name: str, operator_name: str, value: Any):
        """
        Initialize a property query.
        
        Args:
            property_name: Property name to filter on
            operator_name: Operator name (e.g., 'eq', 'lt', 'gt')
            value: Value to compare with
            
        Raises:
            WorkflowQueryError: If the operator is not supported
        """
        if operator_name not in self.OPERATORS:
            raise WorkflowQueryError(f"Unsupported operator: {operator_name}")
        
        self._property_name = property_name
        self._operator_name = operator_name
        self._value = value
        self._operator_func = self.OPERATORS[operator_name]
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            True if the workflow matches, False otherwise
        """
        # Get the property value
        if self._property_name == "workflow_id":
            property_value = workflow.workflow_id
        elif self._property_name == "name":
            property_value = workflow.name
        elif self._property_name == "description":
            property_value = workflow.description
        elif self._property_name == "version":
            property_value = workflow.version
        elif self._property_name == "enabled":
            property_value = workflow.enabled
        elif self._property_name == "step_count":
            property_value = len(workflow.get_steps())
        elif hasattr(workflow, self._property_name):
            property_value = getattr(workflow, self._property_name)
        else:
            # Property not found
            return False
        
        try:
            return self._operator_func(property_value, self._value)
        except Exception:
            # If the comparison fails (e.g., type mismatch), the workflow doesn't match
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "property",
            "property": self._property_name,
            "operator": self._operator_name,
            "value": self._value
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return f"PropertyQuery(property='{self._property_name}', operator='{self._operator_name}', value={self._value})"


class AndQuery(WorkflowQuery):
    """
    Query that combines other queries using AND logic.
    
    This class provides a query that matches workflows matching all of its subqueries.
    """
    
    def __init__(self, *queries: IWorkflowQuery):
        """
        Initialize an AND query.
        
        Args:
            *queries: Subqueries to combine
            
        Raises:
            WorkflowQueryError: If no subqueries are provided
        """
        if not queries:
            raise WorkflowQueryError("AND query must have at least one subquery")
        
        self._queries = queries
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            True if the workflow matches all subqueries, False otherwise
        """
        return all(query.matches(workflow) for query in self._queries)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "and",
            "queries": [query.to_dict() for query in self._queries]
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return f"AndQuery({', '.join(repr(q) for q in self._queries)})"


class OrQuery(WorkflowQuery):
    """
    Query that combines other queries using OR logic.
    
    This class provides a query that matches workflows matching any of its subqueries.
    """
    
    def __init__(self, *queries: IWorkflowQuery):
        """
        Initialize an OR query.
        
        Args:
            *queries: Subqueries to combine
            
        Raises:
            WorkflowQueryError: If no subqueries are provided
        """
        if not queries:
            raise WorkflowQueryError("OR query must have at least one subquery")
        
        self._queries = queries
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            True if the workflow matches any subquery, False otherwise
        """
        return any(query.matches(workflow) for query in self._queries)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "or",
            "queries": [query.to_dict() for query in self._queries]
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return f"OrQuery({', '.join(repr(q) for q in self._queries)})"


class NotQuery(WorkflowQuery):
    """
    Query that negates another query.
    
    This class provides a query that matches workflows not matching its subquery.
    """
    
    def __init__(self, query: IWorkflowQuery):
        """
        Initialize a NOT query.
        
        Args:
            query: Subquery to negate
        """
        self._query = query
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            True if the workflow does not match the subquery, False otherwise
        """
        return not self._query.matches(workflow)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "not",
            "query": self._query.to_dict()
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return f"NotQuery({repr(self._query)})"


class AllQuery(WorkflowQuery):
    """
    Query that matches all workflows.
    
    This class provides a query that matches all workflows in a repository.
    """
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            Always True
        """
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "all"
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return "AllQuery()"


class NoneQuery(WorkflowQuery):
    """
    Query that matches no workflows.
    
    This class provides a query that matches no workflows in a repository.
    """
    
    def matches(self, workflow: IWorkflow) -> bool:
        """
        Check if a workflow matches this query.
        
        Args:
            workflow: Workflow to check
            
        Returns:
            Always False
        """
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary.
        
        Returns:
            Dictionary representation of the query
        """
        return {
            "type": "none"
        }
    
    def __repr__(self) -> str:
        """
        Get a string representation of the query.
        
        Returns:
            String representation
        """
        return "NoneQuery()"


class WorkflowQueryBuilder:
    """
    Builder for creating workflow queries.
    
    This class provides a fluent interface for creating workflow queries,
    with methods for common query operations.
    """
    
    @staticmethod
    def property(property_name: str) -> 'PropertyQueryBuilder':
        """
        Start building a property query.
        
        Args:
            property_name: Property name to filter on
            
        Returns:
            Property query builder
        """
        return PropertyQueryBuilder(property_name)
    
    @staticmethod
    def all() -> AllQuery:
        """
        Create a query that matches all workflows.
        
        Returns:
            Query that matches all workflows
        """
        return AllQuery()
    
    @staticmethod
    def none() -> NoneQuery:
        """
        Create a query that matches no workflows.
        
        Returns:
            Query that matches no workflows
        """
        return NoneQuery()
    
    @staticmethod
    def and_(*queries: IWorkflowQuery) -> AndQuery:
        """
        Create a query that combines other queries using AND logic.
        
        Args:
            *queries: Subqueries to combine
            
        Returns:
            Query that matches workflows matching all subqueries
        """
        return AndQuery(*queries)
    
    @staticmethod
    def or_(*queries: IWorkflowQuery) -> OrQuery:
        """
        Create a query that combines other queries using OR logic.
        
        Args:
            *queries: Subqueries to combine
            
        Returns:
            Query that matches workflows matching any subquery
        """
        return OrQuery(*queries)
    
    @staticmethod
    def not_(query: IWorkflowQuery) -> NotQuery:
        """
        Create a query that negates another query.
        
        Args:
            query: Subquery to negate
            
        Returns:
            Query that matches workflows not matching the subquery
        """
        return NotQuery(query)
    
    @staticmethod
    def from_dict(query_dict: Dict[str, Any]) -> IWorkflowQuery:
        """
        Create a query from a dictionary representation.
        
        Args:
            query_dict: Dictionary representation of a query
            
        Returns:
            Query object
            
        Raises:
            WorkflowQueryError: If the query type is not supported
        """
        query_type = query_dict.get("type")
        
        if query_type == "property":
            return PropertyQuery(
                property_name=query_dict["property"],
                operator_name=query_dict["operator"],
                value=query_dict["value"]
            )
        elif query_type == "and":
            return AndQuery(*[WorkflowQueryBuilder.from_dict(q) for q in query_dict["queries"]])
        elif query_type == "or":
            return OrQuery(*[WorkflowQueryBuilder.from_dict(q) for q in query_dict["queries"]])
        elif query_type == "not":
            return NotQuery(WorkflowQueryBuilder.from_dict(query_dict["query"]))
        elif query_type == "all":
            return AllQuery()
        elif query_type == "none":
            return NoneQuery()
        else:
            raise WorkflowQueryError(f"Unsupported query type: {query_type}")


class PropertyQueryBuilder:
    """
    Builder for creating property queries.
    
    This class provides a fluent interface for creating property queries,
    with methods for different comparison operators.
    """
    
    def __init__(self, property_name: str):
        """
        Initialize a property query builder.
        
        Args:
            property_name: Property name to filter on
        """
        self._property_name = property_name
    
    def eq(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property equals the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "eq", value)
    
    def ne(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property does not equal the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "ne", value)
    
    def lt(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is less than the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "lt", value)
    
    def le(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is less than or equal to the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "le", value)
    
    def gt(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is greater than the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "gt", value)
    
    def ge(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is greater than or equal to the value.
        
        Args:
            value: Value to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "ge", value)
    
    def in_(self, values: List[Any]) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is in the list of values.
        
        Args:
            values: List of values to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "in", values)
    
    def not_in(self, values: List[Any]) -> PropertyQuery:
        """
        Create a query that matches workflows where the property is not in the list of values.
        
        Args:
            values: List of values to compare with
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "not_in", values)
    
    def contains(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property contains the value.
        
        Args:
            value: Value to check for
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "contains", value)
    
    def not_contains(self, value: Any) -> PropertyQuery:
        """
        Create a query that matches workflows where the property does not contain the value.
        
        Args:
            value: Value to check for
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "not_contains", value)
    
    def starts_with(self, value: str) -> PropertyQuery:
        """
        Create a query that matches workflows where the property starts with the value.
        
        Args:
            value: Value to check for
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "starts_with", value)
    
    def ends_with(self, value: str) -> PropertyQuery:
        """
        Create a query that matches workflows where the property ends with the value.
        
        Args:
            value: Value to check for
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "ends_with", value)
    
    def matches(self, pattern: str) -> PropertyQuery:
        """
        Create a query that matches workflows where the property matches the regex pattern.
        
        Args:
            pattern: Regex pattern to match
            
        Returns:
            Property query
        """
        return PropertyQuery(self._property_name, "matches", pattern)
