from datetime import datetime
from typing import cast
import attr
from jinja2 import Environment, FileSystemLoader, Template

env = Environment(loader=FileSystemLoader("templates"), lstrip_blocks=True, trim_blocks=True)

PY_SQL_TYPES = {int: "int", datetime: "timestamp"}


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
    column_type: str = field.metadata.get("type", PY_SQL_TYPES[field.type])

    if field.metadata.get("auto_inc"):
        return _map_auto_inc(column_type)

    return column_type


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

    column_extra_str = " ".join(column_extra)
    return column_extra_str
