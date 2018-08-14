from typing import Type

import attr

from attrs_to_sql.renderer import render
from attrs_to_sql.columns.sql import field_to_column
from .utils import camelcase_to_underscore


def attrs_to_table(attrs: Type) -> str:
    table = camelcase_to_underscore(attrs.__name__)

    fields = attr.fields(attrs)
    columns = map(field_to_column, fields)

    return render("create_table.sql", table=table, columns=columns)
