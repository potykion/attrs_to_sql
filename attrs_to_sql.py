from datetime import datetime
from typing import cast
import attr
from jinja2 import Environment, FileSystemLoader, Template

env = Environment(loader=FileSystemLoader("templates"), lstrip_blocks=True, trim_blocks=True)

PY_SQL_TYPES = {int: "int", datetime: "timestamp", str: "varchar", float: "float"}


def attrs_to_table(attrs: type) -> str:
    fields = attr.fields(attrs)
    columns = map(_field_to_column, fields)

    template: Template = env.get_template("create_table.sql")
    return template.render(columns=columns)


def _field_to_column(field: attr.Attribute) -> str:
    column_name = field.name
    column_type = _build_column_type(field)

    column_str = f"{column_name} {column_type}"

    column_extra = _build_column_extra(field)
    if column_extra:
        column_str = f"{column_str} {column_extra}"

    return column_str


def _build_column_type(field):
    column_type: str = (
        field.metadata.get("type") or PY_SQL_TYPES.get(field.type) or _try_set_array_type(field)
    )

    if not column_type:
        raise ValueError(f"Unsupported type: {field.type}")

    if field.metadata.get("length"):
        return _append_length(column_type, field.metadata.get("length"))

    if field.metadata.get("auto_inc"):
        return _map_auto_inc(column_type)

    return column_type


def _try_set_array_type(field):
    if not issubclass(field.type, list):
        return

    try:
        list_type = field.type.__args__[0]
    except IndexError:
        raise ValueError("No array type provided.")

    list_type = PY_SQL_TYPES.get(list_type)
    if list_type:
        return f"{list_type}[]"


def _append_length(column_type, length):
    if column_type == "varchar":
        return f"varchar({length})"
    else:
        raise ValueError("Only varchar supported.")


def _map_auto_inc(column_type):
    if column_type == "int":
        return "serial"
    elif column_type == "bigint":
        return "bigserial"
    else:
        raise ValueError("Only integer type can be autoincremented.")


def _build_column_extra(field: attr.Attribute) -> str:
    column_extra = []

    if field.metadata.get("primary_key"):
        column_extra.append("PRIMARY KEY")

    has_default = field.default != attr.NOTHING
    immutable_default = not isinstance(field.default, cast(type, attr.Factory))
    if has_default and immutable_default:
        column_extra.append(f"DEFAULT {field.default}")

    if field.metadata.get("not_null"):
        column_extra.append("NOT NULL")

    column_extra_str = " ".join(column_extra)
    return column_extra_str
