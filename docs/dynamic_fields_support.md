# Dynamic Field Support for convert_to_user_format

## Overview

The `convert_to_user_format` function in `lightrag/utils.py` now supports dynamic field extraction from chunks through the `extra_chunk_fields` parameter. This enhancement allows users to include custom fields (like `page_idx`, `section`, etc.) in the output without modifying the core function.

## Motivation

Previously, the function only extracted four fixed fields from chunks:
- `reference_id`
- `content`
- `file_path`
- `chunk_id`

Users who needed additional metadata (such as `page_idx` for page numbers) had to modify the core function, which made maintenance difficult and prevented easy customization.

## Solution

The new `extra_chunk_fields` parameter allows callers to specify a list of additional field names to extract from chunks. This provides:
- **Flexibility**: Add any custom fields on-demand
- **Backward Compatibility**: Existing code continues to work unchanged
- **No Hard-coding**: No need to modify the core function for new fields

## API

### Function Signature

```python
def convert_to_user_format(
    entities_context: list[dict],
    relations_context: list[dict],
    chunks: list[dict],
    references: list[dict],
    query_mode: str,
    entity_id_to_original: dict = None,
    relation_id_to_original: dict = None,
    extra_chunk_fields: list[str] = None,  # NEW parameter
) -> dict[str, Any]:
```

### Parameters

- **extra_chunk_fields** (optional): List of field names to extract from chunks in addition to the standard fields. If a field doesn't exist in a chunk, it will be included with a value of `None`.

## Usage Examples

### Example 1: Basic Usage (Backward Compatible)

Without specifying `extra_chunk_fields`, the function behaves exactly as before:

```python
from lightrag.utils import convert_to_user_format

chunks = [
    {
        "reference_id": "1",
        "content": "Sample text",
        "file_path": "doc.pdf",
        "chunk_id": "chunk-1",
    }
]

result = convert_to_user_format(
    entities_context=[],
    relations_context=[],
    chunks=chunks,
    references=[],
    query_mode="naive",
)

# Output chunks will have only the 4 standard fields
```

### Example 2: Adding page_idx Field

```python
chunks = [
    {
        "reference_id": "1",
        "content": "Text from page 5",
        "file_path": "doc.pdf",
        "chunk_id": "chunk-1",
        "page_idx": 5,  # Additional field
    }
]

result = convert_to_user_format(
    entities_context=[],
    relations_context=[],
    chunks=chunks,
    references=[],
    query_mode="naive",
    extra_chunk_fields=["page_idx"],  # Request page_idx
)

# Output chunk will include page_idx field
# result['data']['chunks'][0]['page_idx'] == 5
```

### Example 3: Multiple Extra Fields

```python
chunks = [
    {
        "reference_id": "1",
        "content": "Introduction",
        "file_path": "paper.pdf",
        "chunk_id": "chunk-1",
        "page_idx": 1,
        "section": "Introduction",
        "author": "Dr. Smith",
        "confidence": 0.95,
    }
]

result = convert_to_user_format(
    entities_context=[],
    relations_context=[],
    chunks=chunks,
    references=[],
    query_mode="naive",
    extra_chunk_fields=["page_idx", "section", "author", "confidence"],
)

# All specified fields will be included in output
```

### Example 4: Handling Missing Fields

If a requested field doesn't exist in a chunk, it will be set to `None`:

```python
chunks = [
    {
        "reference_id": "1",
        "content": "Sample text",
        "file_path": "doc.pdf",
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

# result['data']['chunks'][0]['page_idx'] == None
```

## Integration with RAGAnything or Other Callers

To use this feature in higher-level components:

1. **Configuration Level**: Add `extra_chunk_fields` to your configuration or query parameters
2. **Pass Through**: When calling `convert_to_user_format`, pass the list of fields

Example configuration:

```python
# In your config or QueryParam
query_param.extra_chunk_fields = ["page_idx", "section"]

# When calling convert_to_user_format
result = convert_to_user_format(
    entities_context=entities,
    relations_context=relations,
    chunks=chunks,
    references=references,
    query_mode=query_param.mode,
    extra_chunk_fields=query_param.extra_chunk_fields,  # Pass through
)
```

## Implementation Details

The implementation is minimal and efficient:

1. Standard fields are always extracted first (maintains backward compatibility)
2. If `extra_chunk_fields` is provided and non-empty, each field is extracted using `chunk.get(field, None)`
3. Missing fields default to `None` (safe default that won't break downstream code)

## Testing

Comprehensive test coverage is provided in `tests/test_convert_to_user_format.py`:

- Basic functionality without extra fields (backward compatibility)
- Single and multiple extra fields
- Various data types (int, float, list, dict, bool)
- Missing fields handling
- Empty field lists
- Integration with entities and relations

To run the tests:

```bash
python -m pytest tests/test_convert_to_user_format.py -v
```

## Example Code

A complete working example is available at `examples/example_extra_chunk_fields.py`:

```bash
python examples/example_extra_chunk_fields.py
```

## Backward Compatibility

✅ **Fully backward compatible**: Existing code that doesn't specify `extra_chunk_fields` will continue to work exactly as before.

## Future Extensions

This design allows for easy future enhancements:
- Similar `extra_entity_fields` or `extra_relationship_fields` parameters could be added
- Field validation or type conversion could be added if needed
- Default field lists could be configured globally

## Related Issues

This feature addresses the need for dynamic field extension as described in the problem statement about allowing `aquery/query/aquery_data` to support additional fields like `page_idx` without hard-coding them into the core function.
