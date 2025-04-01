"""
Tests for the workflow query implementation.

This module contains tests for the workflow query implementation.
"""
import unittest
from unittest.mock import Mock

from src.core.workflow.workflow_query import (
    WorkflowQuery, PropertyQuery, AndQuery, OrQuery, NotQuery,
    AllQuery, NoneQuery, WorkflowQueryBuilder
)
from src.core.workflow.service_exceptions import WorkflowQueryError


class TestPropertyQuery(unittest.TestCase):
    """Tests for the PropertyQuery class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock workflow
        self.workflow = Mock()
        self.workflow.workflow_id = "test-workflow"
        self.workflow.name = "Test Workflow"
        self.workflow.description = "Test workflow description"
        self.workflow.version = "1.0.0"
        self.workflow.enabled = True
        self.workflow.get_steps.return_value = [Mock(), Mock(), Mock()]
    
    def test_eq_operator(self):
        """Test the equals operator."""
        query = PropertyQuery("name", "eq", "Test Workflow")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "eq", "Not Test Workflow")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_ne_operator(self):
        """Test the not equals operator."""
        query = PropertyQuery("name", "ne", "Not Test Workflow")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "ne", "Test Workflow")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_contains_operator(self):
        """Test the contains operator."""
        query = PropertyQuery("name", "contains", "Test")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "contains", "Not")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_starts_with_operator(self):
        """Test the starts with operator."""
        query = PropertyQuery("name", "starts_with", "Test")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "starts_with", "Workflow")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_ends_with_operator(self):
        """Test the ends with operator."""
        query = PropertyQuery("name", "ends_with", "Workflow")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "ends_with", "Test")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_matches_operator(self):
        """Test the matches operator."""
        query = PropertyQuery("name", "matches", r"^Test.*")
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("name", "matches", r"^Not.*")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_step_count_property(self):
        """Test querying the step count property."""
        query = PropertyQuery("step_count", "eq", 3)
        
        self.assertTrue(query.matches(self.workflow))
        
        query = PropertyQuery("step_count", "eq", 4)
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_invalid_operator(self):
        """Test an invalid operator."""
        with self.assertRaises(WorkflowQueryError):
            PropertyQuery("name", "invalid", "Test Workflow")
    
    def test_nonexistent_property(self):
        """Test a nonexistent property."""
        query = PropertyQuery("nonexistent", "eq", "value")
        
        self.assertFalse(query.matches(self.workflow))
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query = PropertyQuery("name", "eq", "Test Workflow")
        
        expected = {
            "type": "property",
            "property": "name",
            "operator": "eq",
            "value": "Test Workflow"
        }
        
        self.assertEqual(query.to_dict(), expected)


class TestAndQuery(unittest.TestCase):
    """Tests for the AndQuery class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock workflow
        self.workflow = Mock()
        self.workflow.workflow_id = "test-workflow"
        self.workflow.name = "Test Workflow"
        self.workflow.version = "1.0.0"
        self.workflow.enabled = True
    
    def test_matches(self):
        """Test matching workflows."""
        query1 = PropertyQuery("name", "eq", "Test Workflow")
        query2 = PropertyQuery("version", "eq", "1.0.0")
        query3 = PropertyQuery("version", "eq", "2.0.0")
        
        # Both queries match
        and_query = AndQuery(query1, query2)
        self.assertTrue(and_query.matches(self.workflow))
        
        # One query doesn't match
        and_query = AndQuery(query1, query3)
        self.assertFalse(and_query.matches(self.workflow))
        
        # No queries match
        and_query = AndQuery(query3, query3)
        self.assertFalse(and_query.matches(self.workflow))
    
    def test_empty_query(self):
        """Test an empty AND query."""
        with self.assertRaises(WorkflowQueryError):
            AndQuery()
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query1 = PropertyQuery("name", "eq", "Test Workflow")
        query2 = PropertyQuery("version", "eq", "1.0.0")
        
        and_query = AndQuery(query1, query2)
        
        expected = {
            "type": "and",
            "queries": [query1.to_dict(), query2.to_dict()]
        }
        
        self.assertEqual(and_query.to_dict(), expected)


class TestOrQuery(unittest.TestCase):
    """Tests for the OrQuery class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock workflow
        self.workflow = Mock()
        self.workflow.workflow_id = "test-workflow"
        self.workflow.name = "Test Workflow"
        self.workflow.version = "1.0.0"
        self.workflow.enabled = True
    
    def test_matches(self):
        """Test matching workflows."""
        query1 = PropertyQuery("name", "eq", "Test Workflow")
        query2 = PropertyQuery("version", "eq", "2.0.0")
        query3 = PropertyQuery("name", "eq", "Not Test Workflow")
        
        # One query matches
        or_query = OrQuery(query1, query2)
        self.assertTrue(or_query.matches(self.workflow))
        
        # Both queries match
        or_query = OrQuery(query1, PropertyQuery("version", "eq", "1.0.0"))
        self.assertTrue(or_query.matches(self.workflow))
        
        # No queries match
        or_query = OrQuery(query2, query3)
        self.assertFalse(or_query.matches(self.workflow))
    
    def test_empty_query(self):
        """Test an empty OR query."""
        with self.assertRaises(WorkflowQueryError):
            OrQuery()
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query1 = PropertyQuery("name", "eq", "Test Workflow")
        query2 = PropertyQuery("version", "eq", "1.0.0")
        
        or_query = OrQuery(query1, query2)
        
        expected = {
            "type": "or",
            "queries": [query1.to_dict(), query2.to_dict()]
        }
        
        self.assertEqual(or_query.to_dict(), expected)


class TestNotQuery(unittest.TestCase):
    """Tests for the NotQuery class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock workflow
        self.workflow = Mock()
        self.workflow.workflow_id = "test-workflow"
        self.workflow.name = "Test Workflow"
        self.workflow.version = "1.0.0"
        self.workflow.enabled = True
    
    def test_matches(self):
        """Test matching workflows."""
        query = PropertyQuery("name", "eq", "Test Workflow")
        
        # Query matches, NOT query doesn't
        not_query = NotQuery(query)
        self.assertFalse(not_query.matches(self.workflow))
        
        # Query doesn't match, NOT query does
        query = PropertyQuery("name", "eq", "Not Test Workflow")
        not_query = NotQuery(query)
        self.assertTrue(not_query.matches(self.workflow))
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query = PropertyQuery("name", "eq", "Test Workflow")
        not_query = NotQuery(query)
        
        expected = {
            "type": "not",
            "query": query.to_dict()
        }
        
        self.assertEqual(not_query.to_dict(), expected)


class TestAllQuery(unittest.TestCase):
    """Tests for the AllQuery class."""
    
    def test_matches(self):
        """Test matching workflows."""
        query = AllQuery()
        workflow = Mock()
        
        self.assertTrue(query.matches(workflow))
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query = AllQuery()
        
        expected = {
            "type": "all"
        }
        
        self.assertEqual(query.to_dict(), expected)


class TestNoneQuery(unittest.TestCase):
    """Tests for the NoneQuery class."""
    
    def test_matches(self):
        """Test matching workflows."""
        query = NoneQuery()
        workflow = Mock()
        
        self.assertFalse(query.matches(workflow))
    
    def test_to_dict(self):
        """Test converting the query to a dictionary."""
        query = NoneQuery()
        
        expected = {
            "type": "none"
        }
        
        self.assertEqual(query.to_dict(), expected)


class TestWorkflowQueryBuilder(unittest.TestCase):
    """Tests for the WorkflowQueryBuilder class."""
    
    def test_property(self):
        """Test building a property query."""
        query = WorkflowQueryBuilder.property("name").eq("Test Workflow")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "eq")
        self.assertEqual(query._value, "Test Workflow")
    
    def test_all(self):
        """Test building an all query."""
        query = WorkflowQueryBuilder.all()
        
        self.assertIsInstance(query, AllQuery)
    
    def test_none(self):
        """Test building a none query."""
        query = WorkflowQueryBuilder.none()
        
        self.assertIsInstance(query, NoneQuery)
    
    def test_and(self):
        """Test building an AND query."""
        query1 = WorkflowQueryBuilder.all()
        query2 = WorkflowQueryBuilder.none()
        
        query = WorkflowQueryBuilder.and_(query1, query2)
        
        self.assertIsInstance(query, AndQuery)
        self.assertEqual(query._queries, (query1, query2))
    
    def test_or(self):
        """Test building an OR query."""
        query1 = WorkflowQueryBuilder.all()
        query2 = WorkflowQueryBuilder.none()
        
        query = WorkflowQueryBuilder.or_(query1, query2)
        
        self.assertIsInstance(query, OrQuery)
        self.assertEqual(query._queries, (query1, query2))
    
    def test_not(self):
        """Test building a NOT query."""
        query1 = WorkflowQueryBuilder.all()
        
        query = WorkflowQueryBuilder.not_(query1)
        
        self.assertIsInstance(query, NotQuery)
        self.assertEqual(query._query, query1)
    
    def test_from_dict(self):
        """Test building a query from a dictionary."""
        # Property query
        query_dict = {
            "type": "property",
            "property": "name",
            "operator": "eq",
            "value": "Test Workflow"
        }
        
        query = WorkflowQueryBuilder.from_dict(query_dict)
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "eq")
        self.assertEqual(query._value, "Test Workflow")
        
        # AND query
        query_dict = {
            "type": "and",
            "queries": [
                {
                    "type": "property",
                    "property": "name",
                    "operator": "eq",
                    "value": "Test Workflow"
                },
                {
                    "type": "property",
                    "property": "version",
                    "operator": "eq",
                    "value": "1.0.0"
                }
            ]
        }
        
        query = WorkflowQueryBuilder.from_dict(query_dict)
        
        self.assertIsInstance(query, AndQuery)
        self.assertEqual(len(query._queries), 2)
        self.assertIsInstance(query._queries[0], PropertyQuery)
        self.assertIsInstance(query._queries[1], PropertyQuery)
        
        # Invalid query type
        query_dict = {
            "type": "invalid"
        }
        
        with self.assertRaises(WorkflowQueryError):
            WorkflowQueryBuilder.from_dict(query_dict)


class TestPropertyQueryBuilder(unittest.TestCase):
    """Tests for the PropertyQueryBuilder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = WorkflowQueryBuilder.property("name")
    
    def test_eq(self):
        """Test building an equals query."""
        query = self.builder.eq("Test Workflow")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "eq")
        self.assertEqual(query._value, "Test Workflow")
    
    def test_ne(self):
        """Test building a not equals query."""
        query = self.builder.ne("Test Workflow")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "ne")
        self.assertEqual(query._value, "Test Workflow")
    
    def test_contains(self):
        """Test building a contains query."""
        query = self.builder.contains("Test")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "contains")
        self.assertEqual(query._value, "Test")
    
    def test_starts_with(self):
        """Test building a starts with query."""
        query = self.builder.starts_with("Test")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "starts_with")
        self.assertEqual(query._value, "Test")
    
    def test_ends_with(self):
        """Test building an ends with query."""
        query = self.builder.ends_with("Workflow")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "ends_with")
        self.assertEqual(query._value, "Workflow")
    
    def test_matches(self):
        """Test building a matches query."""
        query = self.builder.matches(r"^Test.*")
        
        self.assertIsInstance(query, PropertyQuery)
        self.assertEqual(query._property_name, "name")
        self.assertEqual(query._operator_name, "matches")
        self.assertEqual(query._value, r"^Test.*")


if __name__ == "__main__":
    unittest.main()
