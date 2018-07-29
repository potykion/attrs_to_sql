from datetime import datetime
from typing import cast, Optional

import attr
from jinja2 import Environment, Template, PackageLoader

from .utils import camelcase_to_underscore, is_optional, is_typing_list, is_typing_dict

env = Environment(
    loader=PackageLoader("attrs_to_sql", "templates"), lstrip_blocks=True, trim_blocks=True
)

PY_SQL_TYPES = {
    int: "int",
    datetime: "timestamp",
    str: "varchar",
    float: "float",
    bool: "boolean",
    dict: "json",
}


def attrs_to_table(attrs: type) -> str:
    table = camelcase_to_underscore(attrs.__name__)

    fields = attr.fields(attrs)
    columns = map(_field_to_column, fields)

    template: Template = env.get_template("create_table.sql")
    return template.render(table=table, columns=columns)


def _field_to_column(field: attr.Attribute) -> str:
    column_name = field.name
    column_type = _build_column_type(field)
    column_str = f"\"{column_name}\" {column_type}"

    column_extra = _build_column_extra(field)
    if column_extra:
        column_str = f"{column_str} {column_extra}"

    return column_str


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
        return "json"

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


def _build_column_extra(field: attr.Attribute) -> str:
    column_extra = []

    if field.metadata.get("primary_key"):
        column_extra.append("PRIMARY KEY")

    default = _try_compute_default(field)
    if default:
        column_extra.append(default)

    if field.metadata.get("not_null"):
        column_extra.append("NOT NULL")

    column_extra_str = " ".join(column_extra)
    return column_extra_str


def _try_compute_default(field: attr.Attribute) -> Optional[str]:
    has_default = field.default != attr.NOTHING and field.default is not None
    immutable_default = not isinstance(field.default, cast(type, attr.Factory))
    if not has_default or not immutable_default:
        return None

    if field.type is bool:
        default_value = "TRUE" if field.default else "FALSE"
    else:
        default_value = str(field.default)

    return f"DEFAULT {default_value}"
