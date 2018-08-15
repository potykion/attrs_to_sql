from datetime import datetime, date, time, timedelta
from decimal import Decimal

import attr
from sqlalchemy.types import *

from attrs_to_sql.columns.converter import ColumnConverter

sa_columns = {
    int: Integer,
    Decimal: Numeric,
    float: Float,
    str: Unicode,
    datetime: DateTime,
    date: Date,
    time: Time,
    timedelta: Interval,
    bytes: Binary,
    bool: Boolean
}

special_columns = [
    (Enum(), str),
    (ARRAY(Integer()), list),
    (JSON(), dict)
]


class SqlAlchemyColumnConverter(ColumnConverter):
    def _build_column_str(self, field: attr.Attribute) -> str:
        return f"sa.Column({self._build_column_name(field)}, {self._build_column_type(field)})"

    def _build_column_type(self, field: attr.Attribute) -> str:
        if field.type in sa_columns:
            return sa_columns[field.type].__name__


if __name__ == '__main__':
    s = "AS"