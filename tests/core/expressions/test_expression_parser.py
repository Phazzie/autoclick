"""Tests for the expression parser"""
import unittest
from typing import Dict, Any

from src.core.expressions.expression_parser import (
    ExpressionParser, TemplateParser, parse_expression, parse_template
)


class TestExpressionParser(unittest.TestCase):
    """Test cases for the expression parser"""

    def test_simple_variable_reference(self):
        """Test parsing a simple variable reference"""
        # Arrange
        context = {"name": "John"}
        expression = "${name}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "John")

    def test_nested_variable_reference(self):
        """Test parsing a nested variable reference"""
        # Arrange
        context = {"user": {"name": "John", "age": 30}}
        expression = "${user.name}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "John")

    def test_array_indexing(self):
        """Test parsing an array index reference"""
        # Arrange
        context = {"items": ["apple", "banana", "cherry"]}
        expression = "${items[1]}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "banana")

    def test_nested_array_indexing(self):
        """Test parsing a nested array index reference"""
        # Arrange
        context = {"users": [{"name": "John"}, {"name": "Jane"}]}
        expression = "${users[1].name}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "Jane")

    def test_multiple_variable_references(self):
        """Test parsing multiple variable references in a string"""
        # Arrange
        context = {"first_name": "John", "last_name": "Doe"}
        expression = "Hello, ${first_name} ${last_name}!"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "Hello, John Doe!")

    def test_missing_variable(self):
        """Test parsing a reference to a missing variable"""
        # Arrange
        context = {"name": "John"}
        expression = "${age}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertIsNone(result)

    def test_missing_nested_variable(self):
        """Test parsing a reference to a missing nested variable"""
        # Arrange
        context = {"user": {"name": "John"}}
        expression = "${user.age}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertIsNone(result)

    def test_missing_array_index(self):
        """Test parsing a reference to a missing array index"""
        # Arrange
        context = {"items": ["apple", "banana"]}
        expression = "${items[2]}"

        # Act
        result = ExpressionParser.parse_expression(expression, context)

        # Assert
        self.assertIsNone(result)

    def test_template_parsing(self):
        """Test parsing a template with variable references"""
        # Arrange
        context = {"name": "John", "age": 30}
        template = "Hello, ${name}! You are ${age} years old."

        # Act
        result = TemplateParser.parse_template(template, context)

        # Assert
        self.assertEqual(result, "Hello, John! You are 30 years old.")

    def test_parse_expression_function(self):
        """Test the parse_expression function"""
        # Arrange
        context = {"name": "John"}
        expression = "${name}"

        # Act
        result = parse_expression(expression, context)

        # Assert
        self.assertEqual(result, "John")

    def test_parse_template_function(self):
        """Test the parse_template function"""
        # Arrange
        context = {"name": "John", "age": 30}
        template = "Hello, ${name}! You are ${age} years old."

        # Act
        result = parse_template(template, context)

        # Assert
        self.assertEqual(result, "Hello, John! You are 30 years old.")


if __name__ == "__main__":
    unittest.main()
