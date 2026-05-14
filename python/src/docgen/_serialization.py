"""JSON serialization helpers for dataclass models."""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any, TypeVar, cast, get_type_hints

T = TypeVar("T")


def _to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    result: list[str] = []
    for i, c in enumerate(name):
        if c.isupper() and i > 0:
            result.append("_")
        result.append(c.lower())
    return "".join(result)


def to_dict(obj: Any) -> Any:
    """Recursively serialize a dataclass to a JSON-compatible dict.

    - Converts snake_case field names to camelCase.
    - Omits None values and empty collections.
    - Converts Enum values to their string value.
    """
    if obj is None:
        return None

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, list):
        items = [to_dict(item) for item in obj]
        return items if items else None

    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            serialized = to_dict(v)
            if serialized is not None:
                result[_to_camel(k) if not k[0].isupper() else k] = serialized
        return result if result else None

    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        result = {}
        for f in dataclasses.fields(obj):
            value = getattr(obj, f.name)
            serialized = to_dict(value)
            if serialized is not None:
                result[f.metadata.get("json_name", _to_camel(f.name))] = serialized
        return result if result else None

    return obj


def from_dict(cls: type[T], data: dict[str, Any]) -> T:
    """Deserialize a JSON dict to a dataclass instance.

    Converts camelCase keys to snake_case to match dataclass fields.
    """
    if not dataclasses.is_dataclass(cls):
        return cast(T, data)

    snake_data = {_to_snake(k): v for k, v in data.items()}
    filtered = {}
    for f in dataclasses.fields(cls):
        aliases = [f.name, f.metadata.get("json_name"), *f.metadata.get("aliases", ())]
        for alias in aliases:
            if alias is None:
                continue
            key = _to_snake(str(alias))
            if key in snake_data:
                filtered[f.name] = snake_data[key]
                break

    # Recursively deserialize nested dataclasses
    hints = get_type_hints(cls)
    for fname, ftype in hints.items():
        if fname in filtered and filtered[fname] is not None:
            origin = getattr(ftype, "__origin__", None)

            # Handle Optional/Union types - extract the non-None type
            actual_type = _unwrap_optional(ftype)
            if actual_type is None:
                continue

            if dataclasses.is_dataclass(actual_type) and isinstance(filtered[fname], dict):
                filtered[fname] = from_dict(cast(type, actual_type), filtered[fname])
            elif origin is list and isinstance(filtered[fname], list):
                inner = _get_list_inner_type(ftype)
                if inner and dataclasses.is_dataclass(inner):
                    filtered[fname] = [
                        from_dict(cast(type, inner), item) if isinstance(item, dict) else item
                        for item in filtered[fname]
                    ]

    return cast(T, cls(**filtered))


def _unwrap_optional(ftype: Any) -> Any:
    """Extract the actual type from Optional[T] / T | None."""
    origin = getattr(ftype, "__origin__", None)
    if origin is not None:
        import types
        if origin is types.UnionType:
            args = ftype.__args__
            non_none = [a for a in args if a is not type(None)]
            return non_none[0] if len(non_none) == 1 else None
    # typing.Union
    if hasattr(ftype, "__args__"):
        args = getattr(ftype, "__args__", ())
        if type(None) in args:
            non_none = [a for a in args if a is not type(None)]
            return non_none[0] if len(non_none) == 1 else None
    if dataclasses.is_dataclass(ftype):
        return ftype
    return None


def _get_list_inner_type(ftype: Any) -> Any:
    """Get the inner type of list[T]."""
    args = getattr(ftype, "__args__", ())
    if args:
        inner = args[0]
        actual = _unwrap_optional(inner)
        return actual if actual else inner
    return None
