from typing import Type

import attr

from attrs_to_sql.columns.converter import ColumnConverter
from attrs_to_sql.columns.sql import SqlColumnConverter
from attrs_to_sql.columns.alchemy import SqlAlchemyColumnConverter
from attrs_to_sql.renderer import render
from .utils import camelcase_to_underscore


@attr.s(auto_attribs=True)
class AttrsConverter:
    template: str
    field_converter: ColumnConverter

    def __call__(self, attrs: Type) -> str:
        table = camelcase_to_underscore(attrs.__name__)

        fields = attr.fields(attrs)
        columns = map(self.field_converter, fields)

        return render(self.template, table=table, columns=columns)


attrs_to_table = attrs_to_create_table = AttrsConverter(
    template="create_table.sql",
    field_converter=SqlColumnConverter()
)

attrs_to_sqlalchemy_table = AttrsConverter(
    template="sqlalchemy_table.py_",
    field_converter=SqlAlchemyColumnConverter()
)
