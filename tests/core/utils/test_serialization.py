"""
Tests for serialization utilities.

This module contains tests for the serialization utilities.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests serialization utilities
"""
import unittest
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

# Import the module to be tested (will be implemented after tests)
# from src.core.utils.serialization import SerializableMixin, Serializer


# Create test classes that will use the mixins
@dataclass
class TestModel:
    """Test model class for serialization tests."""
    id: str
    name: str
    value: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TestSerializableMixin(unittest.TestCase):
    """Tests for the SerializableMixin class."""

    def test_to_dict_not_implemented(self):
        """Test that to_dict raises NotImplementedError if not implemented."""
        # This test will pass once we implement the SerializableMixin
        # with the expected behavior
        from src.core.utils.serialization import SerializableMixin
        
        class TestClass(SerializableMixin):
            pass
            
        test_obj = TestClass()
        with self.assertRaises(NotImplementedError):
            test_obj.to_dict()
            
    def test_from_dict_not_implemented(self):
        """Test that from_dict raises NotImplementedError if not implemented."""
        # This test will pass once we implement the SerializableMixin
        # with the expected behavior
        from src.core.utils.serialization import SerializableMixin
        
        class TestClass(SerializableMixin):
            pass
            
        with self.assertRaises(NotImplementedError):
            TestClass.from_dict({})
            
    def test_validate_required_fields(self):
        """Test that validate_required_fields raises ValueError for missing fields."""
        # This test will pass once we implement the SerializableMixin
        # with the expected behavior
        from src.core.utils.serialization import SerializableMixin
        
        class TestClass(SerializableMixin):
            pass
            
        test_obj = TestClass()
        data = {"field1": "value1"}
        
        # Should not raise for fields that are present
        test_obj.validate_required_fields(data, ["field1"])
        
        # Should raise for fields that are missing
        with self.assertRaises(ValueError):
            test_obj.validate_required_fields(data, ["field2"])
            
        # Should raise for multiple missing fields
        with self.assertRaises(ValueError):
            test_obj.validate_required_fields(data, ["field1", "field2", "field3"])


class TestSerializer(unittest.TestCase):
    """Tests for the Serializer class."""

    def test_to_dict_not_implemented(self):
        """Test that to_dict raises NotImplementedError if not implemented."""
        # This test will pass once we implement the Serializer
        # with the expected behavior
        from src.core.utils.serialization import Serializer
        
        serializer = Serializer(TestModel)
        with self.assertRaises(NotImplementedError):
            serializer.to_dict(TestModel("1", "Test"))
            
    def test_from_dict_not_implemented(self):
        """Test that from_dict raises NotImplementedError if not implemented."""
        # This test will pass once we implement the Serializer
        # with the expected behavior
        from src.core.utils.serialization import Serializer
        
        serializer = Serializer(TestModel)
        with self.assertRaises(NotImplementedError):
            serializer.from_dict({})
            
    def test_validate_required_fields(self):
        """Test that validate_required_fields raises ValueError for missing fields."""
        # This test will pass once we implement the Serializer
        # with the expected behavior
        from src.core.utils.serialization import Serializer
        
        serializer = Serializer(TestModel)
        data = {"field1": "value1"}
        
        # Should not raise for fields that are present
        serializer.validate_required_fields(data, ["field1"])
        
        # Should raise for fields that are missing
        with self.assertRaises(ValueError):
            serializer.validate_required_fields(data, ["field2"])
            
        # Should raise for multiple missing fields
        with self.assertRaises(ValueError):
            serializer.validate_required_fields(data, ["field1", "field2", "field3"])


# Implementation example test (will be used after implementing the mixins)
class TestImplementation(unittest.TestCase):
    """Tests for a concrete implementation of the serialization utilities."""

    def test_serializable_mixin_implementation(self):
        """Test a concrete implementation of SerializableMixin."""
        # This test will be skipped until we implement the SerializableMixin
        # and create a concrete implementation
        try:
            from src.core.utils.serialization import SerializableMixin
            
            class SerializableModel(TestModel, SerializableMixin):
                def to_dict(self) -> Dict[str, Any]:
                    return {
                        "id": self.id,
                        "name": self.name,
                        "value": self.value,
                        "tags": self.tags.copy(),
                        "metadata": self.metadata.copy()
                    }
                    
                @classmethod
                def from_dict(cls, data: Dict[str, Any]) -> 'SerializableModel':
                    cls.validate_required_fields(data, ["id", "name"])
                    return cls(
                        id=data["id"],
                        name=data["name"],
                        value=data.get("value", 0),
                        tags=data.get("tags", []).copy(),
                        metadata=data.get("metadata", {}).copy()
                    )
                    
            # Create a model
            model = SerializableModel("1", "Test", 42, ["tag1", "tag2"], {"key": "value"})
            
            # Convert to dict
            data = model.to_dict()
            
            # Verify the dict
            self.assertEqual(data["id"], "1")
            self.assertEqual(data["name"], "Test")
            self.assertEqual(data["value"], 42)
            self.assertEqual(data["tags"], ["tag1", "tag2"])
            self.assertEqual(data["metadata"], {"key": "value"})
            
            # Convert back to model
            model2 = SerializableModel.from_dict(data)
            
            # Verify the model
            self.assertEqual(model2.id, "1")
            self.assertEqual(model2.name, "Test")
            self.assertEqual(model2.value, 42)
            self.assertEqual(model2.tags, ["tag1", "tag2"])
            self.assertEqual(model2.metadata, {"key": "value"})
            
            # Test missing required fields
            with self.assertRaises(ValueError):
                SerializableModel.from_dict({"name": "Test"})
                
            with self.assertRaises(ValueError):
                SerializableModel.from_dict({"id": "1"})
        except ImportError:
            self.skipTest("SerializableMixin not implemented yet")
            
    def test_serializer_implementation(self):
        """Test a concrete implementation of Serializer."""
        # This test will be skipped until we implement the Serializer
        # and create a concrete implementation
        try:
            from src.core.utils.serialization import Serializer
            
            class TestModelSerializer(Serializer[TestModel]):
                def to_dict(self, obj: TestModel) -> Dict[str, Any]:
                    return {
                        "id": obj.id,
                        "name": obj.name,
                        "value": obj.value,
                        "tags": obj.tags.copy(),
                        "metadata": obj.metadata.copy()
                    }
                    
                def from_dict(self, data: Dict[str, Any]) -> TestModel:
                    self.validate_required_fields(data, ["id", "name"])
                    return TestModel(
                        id=data["id"],
                        name=data["name"],
                        value=data.get("value", 0),
                        tags=data.get("tags", []).copy(),
                        metadata=data.get("metadata", {}).copy()
                    )
                    
            # Create a serializer
            serializer = TestModelSerializer(TestModel)
            
            # Create a model
            model = TestModel("1", "Test", 42, ["tag1", "tag2"], {"key": "value"})
            
            # Convert to dict
            data = serializer.to_dict(model)
            
            # Verify the dict
            self.assertEqual(data["id"], "1")
            self.assertEqual(data["name"], "Test")
            self.assertEqual(data["value"], 42)
            self.assertEqual(data["tags"], ["tag1", "tag2"])
            self.assertEqual(data["metadata"], {"key": "value"})
            
            # Convert back to model
            model2 = serializer.from_dict(data)
            
            # Verify the model
            self.assertEqual(model2.id, "1")
            self.assertEqual(model2.name, "Test")
            self.assertEqual(model2.value, 42)
            self.assertEqual(model2.tags, ["tag1", "tag2"])
            self.assertEqual(model2.metadata, {"key": "value"})
            
            # Test missing required fields
            with self.assertRaises(ValueError):
                serializer.from_dict({"name": "Test"})
                
            with self.assertRaises(ValueError):
                serializer.from_dict({"id": "1"})
        except ImportError:
            self.skipTest("Serializer not implemented yet")


if __name__ == "__main__":
    unittest.main()
