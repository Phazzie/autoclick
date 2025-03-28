"""Parser for variable expressions in strings"""
import re
from typing import Dict, Any, Optional, List, Tuple, Union, Callable


class ExpressionParser:
    """Parser for variable expressions in strings"""

    # Regular expression for finding variable expressions like ${variable} or ${variable.property}
    VARIABLE_PATTERN = r'\${([^{}]+)}'

    @classmethod
    def parse_expression(cls, expression: str, context: Dict[str, Any]) -> Any:
        """
        Parse and evaluate an expression

        Args:
            expression: Expression to parse
            context: Context containing variables

        Returns:
            Evaluated expression result
        """
        # Check if the expression is a simple variable reference
        if expression.startswith("${") and expression.endswith("}"):
            # Extract the variable name
            var_name = expression[2:-1].strip()
            return cls._resolve_variable(var_name, context)

        # Replace all variable references in the string
        def replace_var(match):
            var_name = match.group(1).strip()
            value = cls._resolve_variable(var_name, context)
            return str(value) if value is not None else ""

        return re.sub(cls.VARIABLE_PATTERN, replace_var, expression)

    @classmethod
    def _resolve_variable(cls, var_path: str, context: Dict[str, Any]) -> Any:
        """
        Resolve a variable path to its value

        Args:
            var_path: Variable path (e.g., "user.name" or "items[0]")
            context: Context containing variables

        Returns:
            Variable value or None if not found
        """
        # Handle array indexing and property access
        parts = cls._tokenize_path(var_path)
        
        # Start with the root object
        current = context
        
        for part in parts:
            # Handle array/dict indexing
            if isinstance(part, int):
                if isinstance(current, (list, tuple)) and 0 <= part < len(current):
                    current = current[part]
                elif isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            # Handle property/key access
            elif isinstance(part, str):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                elif hasattr(current, part):
                    current = getattr(current, part)
                else:
                    return None
            # Handle method calls
            elif isinstance(part, tuple) and len(part) == 2:
                method_name, args = part
                if hasattr(current, method_name) and callable(getattr(current, method_name)):
                    method = getattr(current, method_name)
                    current = method(*args)
                else:
                    return None
        
        return current

    @classmethod
    def _tokenize_path(cls, path: str) -> List[Union[str, int, Tuple[str, List[Any]]]]:
        """
        Tokenize a variable path into parts

        Args:
            path: Variable path (e.g., "user.name" or "items[0]")

        Returns:
            List of path parts
        """
        if not path:
            return []

        # Split by dots for property access
        tokens = []
        for part in path.split('.'):
            # Handle array indexing
            if '[' in part and part.endswith(']'):
                name, indices = part.split('[', 1)
                if name:
                    tokens.append(name)
                
                # Extract all indices
                for index in indices.rstrip(']').split(']['):
                    if index.isdigit():
                        tokens.append(int(index))
                    else:
                        tokens.append(index)
            # Handle method calls
            elif '(' in part and part.endswith(')'):
                name, args_str = part.split('(', 1)
                args_str = args_str.rstrip(')')
                
                # Parse arguments
                args = []
                if args_str:
                    for arg in args_str.split(','):
                        arg = arg.strip()
                        if arg.isdigit():
                            args.append(int(arg))
                        elif arg.lower() == 'true':
                            args.append(True)
                        elif arg.lower() == 'false':
                            args.append(False)
                        elif arg.lower() == 'null' or arg.lower() == 'none':
                            args.append(None)
                        elif (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                            args.append(arg[1:-1])
                        else:
                            args.append(arg)
                
                tokens.append((name, args))
            else:
                tokens.append(part)
        
        return tokens


class TemplateParser:
    """Parser for templates with variable expressions"""

    @classmethod
    def parse_template(cls, template: str, context: Dict[str, Any]) -> str:
        """
        Parse a template string and replace variable expressions

        Args:
            template: Template string with variable expressions
            context: Context containing variables

        Returns:
            Parsed template with variables replaced
        """
        return ExpressionParser.parse_expression(template, context)


def parse_expression(expression: str, context: Dict[str, Any]) -> Any:
    """
    Parse and evaluate an expression

    Args:
        expression: Expression to parse
        context: Context containing variables

    Returns:
        Evaluated expression result
    """
    return ExpressionParser.parse_expression(expression, context)


def parse_template(template: str, context: Dict[str, Any]) -> str:
    """
    Parse a template string and replace variable expressions

    Args:
        template: Template string with variable expressions
        context: Context containing variables

    Returns:
        Parsed template with variables replaced
    """
    return TemplateParser.parse_template(template, context)
