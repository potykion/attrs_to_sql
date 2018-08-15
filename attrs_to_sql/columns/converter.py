from typing import Union, Type, cast, Optional, Any

import attr

from attrs_to_sql.utils import is_optional


class ColumnConverter:
    # todo _build_column_name, _build_column_type as properties
    # todo field as class field

    def __call__(self, field: attr.Attribute) -> str:
        return self._build_column_str(field)

    def _build_column_str(self, field: attr.Attribute) -> str:
        raise NotImplementedError()

    def _build_column_name(self, field: attr.Attribute) -> str:
        return f'"{field.name}"'

    def _build_column_type(self, field: attr.Attribute) -> str:
        raise NotImplementedError()


def extract_field_type(field: Union[attr.Attribute, Type]) -> Type:
    type_ = field.type if isinstance(field, attr.Attribute) else field
    type_ = cast(Type, type_)

    if is_optional(type_):
        type_ = cast(Union[Type, Any], type_)
        type_ = type_.__args__[0]

    type_ = cast(Type, type_)
    return type_
