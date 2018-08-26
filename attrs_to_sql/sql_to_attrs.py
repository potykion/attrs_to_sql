from typing import Iterable

import sqlalchemy as sa
from sqlalchemy import ColumnDefault
from sqlalchemy.sql.type_api import TypeEngine

from attrs_to_sql.renderer import render


def sqlalchemy_to_attrs(table: sa.Table, class_name: str = None) -> str:
    title = class_name or table.name
    fields = list(_build_fields(table.columns))
    return render("attrs.py_", title=title, fields=fields)


def _build_fields(columns: Iterable[sa.Column]) -> Iterable[str]:
    for column in columns:
        column_name = column.name

        column_type_str = _build_column_type_str(column.type)

        column_default = _build_column_default(column)

        yield f"{column_name}: {column_type_str}{column_default}"


def _build_column_type_str(column_type: TypeEngine) -> str:
    if isinstance(column_type, sa.ARRAY):
        item_type = _build_column_type_str(column_type.item_type)
        return f"List[{item_type}]"

    if isinstance(column_type, sa.JSON):
        return "Dict"

    return column_type.python_type.__name__


def _build_column_default(column: sa.Column) -> str:
    if column.default:
        column_default: ColumnDefault = column.default
        return f" = {column_default.arg}"

    return ""
