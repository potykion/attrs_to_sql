import attr
from jinja2 import Environment, FileSystemLoader, Template

env = Environment(loader=FileSystemLoader("templates"), lstrip_blocks=True, trim_blocks=True)

PY_SQL_TYPES = {int: "int"}


def attrs_to_table(attrs: type) -> str:
    fields = attr.fields(attrs)
    columns = map(_field_to_column, fields)

    template: Template = env.get_template("create_table.sql")
    return template.render(columns=columns)


def _field_to_column(field: attr.Attribute) -> str:
    column_name = field.name
    column_type = _build_column_type(field)
    column_extra = _build_column_extra(field)
    return f"{column_name} {column_type} {column_extra}"


def _build_column_type(field):
    return field.metadata.get("type", PY_SQL_TYPES[field.type])


def _build_column_extra(field: attr.Attribute) -> str:
    column_extra = []

    if field.metadata.get("primary_key"):
        column_extra.append("PRIMARY KEY")

    if field.default != attr.NOTHING:
        column_extra.append(f"DEFAULT {field.default}")

    column_extra_str = " ".join(column_extra)
    return column_extra_str
