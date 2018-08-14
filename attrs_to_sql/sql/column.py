from datetime import datetime
from enum import IntEnum
from typing import Optional, cast

import attr

from attrs_to_sql.utils import is_optional, is_typing_dict, is_typing_list, join_not_none

PY_SQL_TYPES = {
    int: "int",
    IntEnum: "int",
    datetime: "timestamp",
    str: "varchar",
    float: "float",
    bool: "boolean",
    dict: "json",
}


def field_to_column(field: attr.Attribute) -> str:
    return join_not_none(
        [_build_column_name(field), _build_column_type(field), _build_column_extra(field)]
    )


# column name


def _build_column_name(field: attr.Attribute) -> str:
    return f'"{field.name}"'


# column type


def _build_column_type(field: attr.Attribute) -> str:
    column_type = _try_identify_sql_type(field)
    if not column_type:
        raise ValueError(f"Unsupported type: {field.type}")

    if field.metadata.get("length"):
        return _append_length(column_type, cast(int, field.metadata.get("length")))

    if field.metadata.get("auto_inc"):
        return _map_auto_inc(column_type)

    return column_type


def _try_identify_sql_type(field):
    if field.metadata.get("type"):
        return str(field.metadata.get("type"))

    if is_optional(field.type):
        python_type = field.type.__args__[0]
    else:
        python_type = field.type

    if PY_SQL_TYPES.get(python_type):
        return PY_SQL_TYPES.get(python_type)

    return _try_set_json_type(field) or _try_set_array_type(field)


def _try_set_json_type(field: attr.Attribute) -> Optional[str]:
    is_dict_type = is_typing_dict(field.type)
    if is_dict_type:
        return "json"

    list_type = _try_extract_list_type(field.type)
    is_dict_type = is_typing_dict(list_type)
    if is_dict_type:
        return "json[]"

    return None


def _try_set_array_type(field: attr.Attribute) -> Optional[str]:
    if not is_typing_list(field.type):
        return None

    list_type = _try_extract_list_type(field.type)

    sql_type = PY_SQL_TYPES.get(list_type)
    if not sql_type:
        return None

    return f"{sql_type}[]"


def _try_extract_list_type(list_type):
    try:
        return list_type.__args__[0]  # type: ignore
    except IndexError:
        raise ValueError("No array type provided.")


def _append_length(column_type: str, length: int) -> str:
    if column_type == "varchar":
        return f"varchar({length})"

    raise ValueError("Only varchar supported.")


def _map_auto_inc(column_type: str) -> str:
    if column_type == "int":
        return "serial"

    if column_type == "bigint":
        return "bigserial"

    raise ValueError("Only integer type can be autoincremented.")


# column extra (pk, default, not null)


def _build_column_extra(field: attr.Attribute) -> str:
    return join_not_none(
        [
            "PRIMARY KEY" if _check_is_pk(field) else None,
            "NOT NULL" if _check_is_not_null(field) else None,
            _try_compute_default(field),
        ]
    )


def _check_is_pk(field: attr.Attribute) -> bool:
    return bool(field.metadata.get("primary_key"))


def _check_is_not_null(field: attr.Attribute) -> bool:
    return bool(field.metadata.get("not_null"))


def _try_compute_default(field: attr.Attribute) -> Optional[str]:
    has_default = field.default != attr.NOTHING and field.default is not None
    immutable_default = not isinstance(field.default, cast(type, attr.Factory))
    if not has_default or not immutable_default:
        return None

    if field.type is bool:
        default_value = "TRUE" if field.default else "FALSE"
    elif field.type is IntEnum:
        default_value = str(int(cast(int, field.default)))
    else:
        default_value = str(field.default)

    return f"DEFAULT {default_value}"
