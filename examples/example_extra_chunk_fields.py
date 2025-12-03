"""
Example: Using extra_chunk_fields with convert_to_user_format

This example demonstrates how to use the extra_chunk_fields parameter
to include additional dynamic fields (like page_idx) in the chunk output.
"""

from lightrag.utils import convert_to_user_format


def example_basic_usage():
    """Basic example without extra fields (backward compatible)."""
    print("=" * 60)
    print("Example 1: Basic usage without extra fields")
    print("=" * 60)
    
    chunks = [
        {
            "reference_id": "1",
            "content": "This is the first chunk of text.",
            "file_path": "document1.pdf",
            "chunk_id": "chunk-001",
        },
    ]
    
    result = convert_to_user_format(
        entities_context=[],
        relations_context=[],
        chunks=chunks,
        references=[],
        query_mode="naive",
    )
    
    print(f"Status: {result['status']}")
    print(f"Number of chunks: {len(result['data']['chunks'])}")
    print(f"First chunk fields: {list(result['data']['chunks'][0].keys())}")
    print(f"First chunk: {result['data']['chunks'][0]}")
    print()


def example_with_page_idx():
    """Example with page_idx field."""
    print("=" * 60)
    print("Example 2: Adding page_idx field")
    print("=" * 60)
    
    chunks = [
        {
            "reference_id": "1",
            "content": "This is content from page 5.",
            "file_path": "document1.pdf",
            "chunk_id": "chunk-001",
            "page_idx": 5,  # Additional field
        },
        {
            "reference_id": "1",
            "content": "This is content from page 6.",
            "file_path": "document1.pdf",
            "chunk_id": "chunk-002",
            "page_idx": 6,  # Additional field
        },
    ]
    
    result = convert_to_user_format(
        entities_context=[],
        relations_context=[],
        chunks=chunks,
        references=[],
        query_mode="naive",
        extra_chunk_fields=["page_idx"],  # Specify the extra field to include
    )
    
    print(f"Status: {result['status']}")
    print(f"Number of chunks: {len(result['data']['chunks'])}")
    print(f"First chunk fields: {list(result['data']['chunks'][0].keys())}")
    
    for i, chunk in enumerate(result['data']['chunks'], 1):
        print(f"\nChunk {i}:")
        print(f"  Content: {chunk['content'][:30]}...")
        print(f"  Page index: {chunk['page_idx']}")
    print()


def example_with_multiple_fields():
    """Example with multiple extra fields."""
    print("=" * 60)
    print("Example 3: Adding multiple extra fields")
    print("=" * 60)
    
    chunks = [
        {
            "reference_id": "1",
            "content": "Introduction to the topic.",
            "file_path": "research_paper.pdf",
            "chunk_id": "chunk-001",
            "page_idx": 1,
            "section": "Introduction",
            "author": "Dr. Smith",
            "confidence": 0.95,
        },
        {
            "reference_id": "1",
            "content": "Methodology description.",
            "file_path": "research_paper.pdf",
            "chunk_id": "chunk-002",
            "page_idx": 5,
            "section": "Methodology",
            "author": "Dr. Smith",
            "confidence": 0.88,
        },
    ]
    
    # Specify multiple fields to include
    result = convert_to_user_format(
        entities_context=[],
        relations_context=[],
        chunks=chunks,
        references=[],
        query_mode="naive",
        extra_chunk_fields=["page_idx", "section", "author", "confidence"],
    )
    
    print(f"Status: {result['status']}")
    print(f"Number of chunks: {len(result['data']['chunks'])}")
    print(f"First chunk fields: {list(result['data']['chunks'][0].keys())}")
    
    for i, chunk in enumerate(result['data']['chunks'], 1):
        print(f"\nChunk {i}:")
        print(f"  Section: {chunk['section']}")
        print(f"  Page: {chunk['page_idx']}")
        print(f"  Author: {chunk['author']}")
        print(f"  Confidence: {chunk['confidence']}")
        print(f"  Content: {chunk['content'][:30]}...")
    print()


def example_missing_field():
    """Example showing graceful handling of missing fields."""
    print("=" * 60)
    print("Example 4: Handling missing fields gracefully")
    print("=" * 60)
    
    chunks = [
        {
            "reference_id": "1",
            "content": "This chunk has page_idx.",
            "file_path": "doc1.pdf",
            "chunk_id": "chunk-001",
            "page_idx": 3,
        },
        {
            "reference_id": "1",
            "content": "This chunk is missing page_idx.",
            "file_path": "doc1.pdf",
            "chunk_id": "chunk-002",
            # page_idx is missing
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
    
    for i, chunk in enumerate(result['data']['chunks'], 1):
        print(f"\nChunk {i}:")
        print(f"  Content: {chunk['content'][:40]}")
        print(f"  Page index: {chunk['page_idx']}")  # Will be None if missing
    print()


if __name__ == "__main__":
    example_basic_usage()
    example_with_page_idx()
    example_with_multiple_fields()
    example_missing_field()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
