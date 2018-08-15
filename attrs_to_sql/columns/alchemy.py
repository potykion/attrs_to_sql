from datetime import datetime, date, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Type, Union

import attr
import sqlalchemy as sa
from attrs_to_sql.columns.converter import ColumnConverter, extract_field_type
from attrs_to_sql.utils import is_typing_dict, is_typing_list, is_optional

simple_types = {
    int: sa.Integer,
    Decimal: sa.Numeric,
    float: sa.Float,
    str: sa.Unicode,
    datetime: sa.DateTime,
    date: sa.Date,
    time: sa.Time,
    timedelta: sa.Interval,
    bytes: sa.Binary,
    bool: sa.Boolean
}


class SqlAlchemyColumnConverter(ColumnConverter):
    def _build_column_str(self, field: attr.Attribute) -> str:
        return f"sa.Column({self._build_column_name(field)}, {self._build_column_type(field)})"

    def _build_column_type(self, field: Union[attr.Attribute, Type]) -> str:
        type_ = extract_field_type(field)

        if type_ in simple_types:
            return f"sa.{simple_types[type_].__name__}"

        if issubclass(type_, Enum):
            return f"sa.Enum({type_.__name__})"

        if is_typing_dict(type_):
            return "sa.JSON"

        if is_typing_list(type_):
            array_type = self._build_column_type(type_.__args__[0])
            return f"sa.ARRAY({array_type})"


