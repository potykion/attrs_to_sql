import attr
from jinja2 import Environment, Template, PackageLoader

from attrs_to_sql.sql.column import field_to_column
from .utils import camelcase_to_underscore

env = Environment(
    loader=PackageLoader("attrs_to_sql", "templates"), lstrip_blocks=True, trim_blocks=True
)


def attrs_to_table(attrs: type) -> str:
    table = camelcase_to_underscore(attrs.__name__)

    fields = attr.fields(attrs)
    columns = map(field_to_column, fields)

    template: Template = env.get_template("create_table.sql")
    return template.render(table=table, columns=columns)
