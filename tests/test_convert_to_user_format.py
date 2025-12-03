"""
Tests for convert_to_user_format function with dynamic field support.

This module tests the convert_to_user_format function's ability to handle
extra chunk fields dynamically, as well as its backward compatibility.
"""

import pytest
from lightrag.utils import convert_to_user_format


class TestConvertToUserFormatBasic:
    """Test basic functionality of convert_to_user_format without extra fields."""

    def test_basic_conversion_without_extra_fields(self):
        """Test basic conversion maintains backward compatibility."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content 1",
                "file_path": "test1.txt",
                "chunk_id": "chunk-1",
            },
            {
                "reference_id": "2",
                "content": "Test content 2",
                "file_path": "test2.txt",
                "chunk_id": "chunk-2",
            },
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
        )

        assert result["status"] == "success"
        assert len(result["data"]["chunks"]) == 2
        
        # Verify basic fields are present
        for i, chunk in enumerate(result["data"]["chunks"]):
            assert "reference_id" in chunk
            assert "content" in chunk
            assert "file_path" in chunk
            assert "chunk_id" in chunk
            assert chunk["reference_id"] == chunks[i]["reference_id"]
            assert chunk["content"] == chunks[i]["content"]

    def test_empty_chunks(self):
        """Test handling of empty chunks list."""
        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=[],
            references=[],
            query_mode="naive",
        )

        assert result["status"] == "success"
        assert len(result["data"]["chunks"]) == 0

    def test_chunks_with_missing_fields(self):
        """Test handling of chunks with missing standard fields."""
        chunks = [
            {
                "content": "Test content",
                # Missing reference_id, file_path, and chunk_id
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
        )

        assert result["status"] == "success"
        assert len(result["data"]["chunks"]) == 1
        chunk = result["data"]["chunks"][0]
        
        # Verify default values are applied
        assert chunk["reference_id"] == ""
        assert chunk["content"] == "Test content"
        assert chunk["file_path"] == "unknown_source"
        assert chunk["chunk_id"] == ""


class TestConvertToUserFormatExtraFields:
    """Test dynamic extra_chunk_fields functionality."""

    def test_single_extra_field(self):
        """Test adding a single extra field to chunks."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                "page_idx": 5,
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=["page_idx"],
        )

        assert result["status"] == "success"
        chunk = result["data"]["chunks"][0]
        
        # Verify standard fields
        assert chunk["reference_id"] == "1"
        assert chunk["content"] == "Test content"
        assert chunk["file_path"] == "test.txt"
        assert chunk["chunk_id"] == "chunk-1"
        
        # Verify extra field
        assert "page_idx" in chunk
        assert chunk["page_idx"] == 5

    def test_multiple_extra_fields(self):
        """Test adding multiple extra fields to chunks."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                "page_idx": 5,
                "section": "Introduction",
                "author": "John Doe",
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=["page_idx", "section", "author"],
        )

        chunk = result["data"]["chunks"][0]
        
        # Verify all extra fields
        assert chunk["page_idx"] == 5
        assert chunk["section"] == "Introduction"
        assert chunk["author"] == "John Doe"

    def test_extra_field_not_in_chunk(self):
        """Test handling when extra field is not present in chunk."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                # page_idx is missing
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=["page_idx"],
        )

        chunk = result["data"]["chunks"][0]
        
        # Verify field is present with None value
        assert "page_idx" in chunk
        assert chunk["page_idx"] is None

    def test_empty_extra_fields_list(self):
        """Test that empty extra_chunk_fields list behaves like None."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                "page_idx": 5,
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=[],
        )

        chunk = result["data"]["chunks"][0]
        
        # Verify extra field is NOT included
        assert "page_idx" not in chunk

    def test_extra_fields_with_various_types(self):
        """Test extra fields with various data types."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                "page_idx": 5,  # int
                "confidence": 0.95,  # float
                "tags": ["science", "research"],  # list
                "metadata": {"key": "value"},  # dict
                "is_verified": True,  # bool
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=["page_idx", "confidence", "tags", "metadata", "is_verified"],
        )

        chunk = result["data"]["chunks"][0]
        
        # Verify all types are preserved
        assert chunk["page_idx"] == 5
        assert chunk["confidence"] == 0.95
        assert chunk["tags"] == ["science", "research"]
        assert chunk["metadata"] == {"key": "value"}
        assert chunk["is_verified"] is True

    def test_multiple_chunks_with_extra_fields(self):
        """Test multiple chunks each with their own extra field values."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Content 1",
                "file_path": "test1.txt",
                "chunk_id": "chunk-1",
                "page_idx": 1,
            },
            {
                "reference_id": "2",
                "content": "Content 2",
                "file_path": "test2.txt",
                "chunk_id": "chunk-2",
                "page_idx": 2,
            },
            {
                "reference_id": "3",
                "content": "Content 3",
                "file_path": "test3.txt",
                "chunk_id": "chunk-3",
                # Missing page_idx
            },
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            extra_chunk_fields=["page_idx"],
        )

        assert len(result["data"]["chunks"]) == 3
        assert result["data"]["chunks"][0]["page_idx"] == 1
        assert result["data"]["chunks"][1]["page_idx"] == 2
        assert result["data"]["chunks"][2]["page_idx"] is None

    def test_extra_fields_do_not_override_standard_fields(self):
        """Test that extra_chunk_fields don't override standard fields."""
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
            }
        ]

        result = convert_to_user_format(
            entities_context=[],
            relations_context=[],
            chunks=chunks,
            references=[],
            query_mode="naive",
            # Try to "add" standard fields via extra_chunk_fields
            extra_chunk_fields=["content", "chunk_id"],
        )

        chunk = result["data"]["chunks"][0]
        
        # Standard fields should still be set correctly
        # (extra_chunk_fields processing happens AFTER standard fields)
        assert chunk["content"] == "Test content"
        assert chunk["chunk_id"] == "chunk-1"


class TestConvertToUserFormatIntegration:
    """Test convert_to_user_format with entities, relations, and chunks."""

    def test_full_conversion_with_extra_fields(self):
        """Test complete conversion with all data types and extra fields."""
        entities = [{"entity": "Entity1"}]
        relations = [{"entity1": "Entity1", "entity2": "Entity2"}]
        chunks = [
            {
                "reference_id": "1",
                "content": "Test content",
                "file_path": "test.txt",
                "chunk_id": "chunk-1",
                "page_idx": 10,
                "section": "Chapter 1",
            }
        ]
        references = [{"reference_id": "1", "file_path": "test.txt"}]

        result = convert_to_user_format(
            entities_context=entities,
            relations_context=relations,
            chunks=chunks,
            references=references,
            query_mode="hybrid",
            extra_chunk_fields=["page_idx", "section"],
        )

        assert result["status"] == "success"
        assert result["metadata"]["query_mode"] == "hybrid"
        assert len(result["data"]["entities"]) == 1
        assert len(result["data"]["relationships"]) == 1
        assert len(result["data"]["chunks"]) == 1
        assert len(result["data"]["references"]) == 1
        
        # Verify chunk has extra fields
        chunk = result["data"]["chunks"][0]
        assert chunk["page_idx"] == 10
        assert chunk["section"] == "Chapter 1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
