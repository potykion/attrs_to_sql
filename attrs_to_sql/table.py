from typing import Type

import attr

from attrs_to_sql.columns import (
    FieldToColumnConverter,
    SqlAlchemyColumnConverter,
    CreateTableSqlColumnConverter,
)
from attrs_to_sql.renderer import render
from .utils import camelcase_to_underscore


@attr.s(auto_attribs=True)
class AttrsConverter:
    template: str
    field_converter: FieldToColumnConverter

    def __call__(self, attrs: Type) -> str:
        table = camelcase_to_underscore(attrs.__name__)

        fields = attr.fields(attrs)
        columns = map(self.field_converter, fields)

        return render(self.template, table=table, columns=columns)


attrs_to_table = attrs_to_create_table = AttrsConverter(
    template="create_table.sql", field_converter=CreateTableSqlColumnConverter()
)

attrs_to_sqlalchemy_table = AttrsConverter(
    template="sqlalchemy_table.py_", field_converter=SqlAlchemyColumnConverter()
)
