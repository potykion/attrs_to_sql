from datetime import datetime, date, time, timedelta
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Dict, Type, Optional, cast, List

import attr

from attrs_to_sql.utils import is_typing_dict, is_typing_list, join_not_none, extract_field_type


class FieldToColumnConverter:
    type_converters = ["_try_as_simple", "_try_as_enum", "_try_as_json", "_try_as_list"]

    simple_types: Dict[Type, str]

    def __call__(self, field: attr.Attribute) -> str:
        column_name = f'"{field.name}"'
        column_type = self._build_column_type(field)
        column_type = self._append_column_extra(field, column_type)
        return self._build_column_str(column_name, column_type)

    def _build_column_str(self, column_name: str, column_type: str) -> str:
        raise NotImplementedError()

    def _build_column_type(self, field: attr.Attribute) -> str:
        type_ = extract_field_type(field)
        converted = map(lambda converter: getattr(self, converter)(type_), self.type_converters)

        try:
            return next(filter(None, converted))
        except StopIteration:
            raise ValueError(f"Unsupported field type: {field.type}")

    def _append_column_extra(self, field: attr.Attribute, column_type: str) -> str:
        return column_type

    # type checkers

    def _try_as_simple(self, type_: Type) -> Optional[str]:
        try:
            return self._type_to_simple(type_)
        except KeyError:
            return None

    def _try_as_enum(self, type_: Type) -> Optional[str]:
        if issubclass(type_, Enum):
            return self._type_to_enum(type_)

        return None

    def _try_as_json(self, type_: Type) -> Optional[str]:
        if is_typing_dict(type_):
            return self._type_to_json(type_)

        return None

    def _try_as_list(self, type_: Type) -> Optional[str]:
        if is_typing_list(type_):
            array_type = self.__extract_list_type(type_)
            return self._type_to_array(type_, array_type)

        return None

    def __extract_list_type(self, type_: Type[List]) -> str:
        try:
            return self._build_column_type(getattr(type_, "__args__")[0])
        except IndexError:
            raise ValueError("No array type provided.")

    # type converters

    def _type_to_simple(self, type_: Type) -> str:
        raise NotImplementedError()

    def _type_to_enum(self, type_: type) -> str:
        raise NotImplementedError()

    def _type_to_json(self, type_: type) -> str:
        raise NotImplementedError()

    def _type_to_array(self, type_: type, array_type: str) -> str:
        raise NotImplementedError()


class SqlAlchemyColumnConverter(FieldToColumnConverter):
    def _build_column_str(self, column_name: str, column_type: str) -> str:
        return f"sa.Column({column_name}, {column_type})"

    def _type_to_simple(self, type_: Type) -> str:
        return {
            int: "sa.Integer",
            Decimal: "sa.Numeric",
            float: "sa.Float",
            str: "sa.Unicode",
            datetime: "sa.DateTime",
            date: "sa.Date",
            time: "sa.Time",
            timedelta: "sa.Interval",
            bytes: "sa.Binary",
            bool: "sa.Boolean",
        }[type_]

    def _type_to_enum(self, type_: Type) -> str:
        return f"sa.Enum({type_.__name__})"

    def _type_to_json(self, type_: Type) -> str:
        return "sa.JSON"

    def _type_to_array(self, type_: Type, array_type: str) -> str:
        return f"sa.ARRAY({array_type})"


class CreateTableSqlColumnConverter(FieldToColumnConverter):
    def _build_column_str(self, column_name: str, column_type: str) -> str:
        return f"{column_name} {column_type}"

    def _build_column_type(self, field: attr.Attribute) -> str:
        if isinstance(field, attr.Attribute) and field.metadata.get("type"):
            return str(field.metadata["type"])

        return super(CreateTableSqlColumnConverter, self)._build_column_type(field)

    def _append_column_extra(self, field: attr.Attribute, column_type: str) -> str:
        column_type = self._modify_type(field, column_type)

        column_extra = join_not_none(
            [
                "PRIMARY KEY" if _check_is_pk(field) else None,
                "NOT NULL" if _check_is_not_null(field) else None,
                _try_compute_default(field),
            ]
        )
        if column_extra:
            column_type = f"{column_type} {column_extra}"

        return column_type

    def _modify_type(self, field: attr.Attribute, column_type: str) -> str:
        if column_type == "varchar":
            length = field.metadata.get("length")
            return f"varchar({length})"

        if column_type in ["int", "bigint"]:
            if field.metadata.get("auto_inc"):
                return column_type.replace("int", "serial")

        return column_type

    def _type_to_simple(self, type_: Type) -> str:
        return {int: "int", datetime: "timestamp", str: "varchar", float: "float", bool: "boolean"}[
            type_
        ]

    def _type_to_enum(self, type_: Type) -> str:
        if issubclass(type_, IntEnum):
            return "int"

        return "str"

    def _type_to_json(self, type_: Type) -> str:
        return "json"

    def _type_to_array(self, type_: Type, array_type: str) -> str:
        return f"{array_type}[]"


def _check_is_pk(field: attr.Attribute) -> bool:
    return bool(field.metadata.get("primary_key"))


def _check_is_not_null(field: attr.Attribute) -> bool:
    return bool(field.metadata.get("not_null"))


def _try_compute_default(field: attr.Attribute) -> Optional[str]:
    has_default = field.default != attr.NOTHING and field.default is not None
    immutable_default = not isinstance(field.default, cast(type, attr.Factory))
    if not has_default or not immutable_default:
        return None

    type_ = extract_field_type(field)
    if type_ is bool:
        default_value = "TRUE" if field.default else "FALSE"
    elif issubclass(type_, IntEnum):
        default_value = str(int(cast(int, field.default)))
    else:
        default_value = str(field.default)

    return f"DEFAULT {default_value}"
