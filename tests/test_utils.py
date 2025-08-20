"""Unit tests for the utils module."""
import unittest
from mcp_sp_snowflake_server.utils import (
    validate_sp_name,
    split_sp_name,
    split_schema_name,
    validate_schema_name
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_validate_sp_name_valid(self):
        """Test that valid stored procedure names are accepted."""
        self.assertTrue(validate_sp_name("DB.SCHEMA.PROCEDURE"))
        self.assertTrue(validate_sp_name("test_db.test_schema.test_procedure"))

    def test_validate_sp_name_invalid(self):
        """Test that invalid stored procedure names are rejected."""
        with self.assertRaises(ValueError):
            validate_sp_name("INVALID_FORMAT")
        with self.assertRaises(ValueError):
            validate_sp_name("DB.SCHEMA")
        with self.assertRaises(ValueError):
            validate_sp_name("DB.SCHEMA.PROCEDURE.EXTRA")

    def test_split_sp_name(self):
        """Test splitting of stored procedure names."""
        db, schema, name = split_sp_name("DB.SCHEMA.PROCEDURE")
        self.assertEqual(db, "DB")
        self.assertEqual(schema, "SCHEMA")
        self.assertEqual(name, "PROCEDURE")

    def test_split_schema_name(self):
        """Test splitting of schema names."""
        db, schema = split_schema_name("DB.SCHEMA")
        self.assertEqual(db, "DB")
        self.assertEqual(schema, "SCHEMA")

    def test_validate_schema_name_valid(self):
        """Test that valid schema names are accepted."""
        self.assertTrue(validate_schema_name("DB.SCHEMA"))
        self.assertTrue(validate_schema_name("test_db.test_schema"))

    def test_validate_schema_name_invalid(self):
        """Test that invalid schema names are rejected."""
        with self.assertRaises(ValueError):
            validate_schema_name("INVALID_FORMAT")
        with self.assertRaises(ValueError):
            validate_schema_name("DB.SCHEMA.EXTRA")


if __name__ == '__main__':
    unittest.main()