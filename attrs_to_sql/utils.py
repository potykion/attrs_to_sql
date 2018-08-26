import re
import typing
from typing import Union, Type, cast, Any, List

import attr


def camelcase_to_underscore(camelcase: str) -> str:
    """https://stackoverflow.com/a/1176023"""
    underscored = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camelcase)
    underscored = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", underscored)
    lowered = underscored.lower()
    return lowered


def is_optional(type_: typing.Type) -> bool:
    return bool(re.match(r"^typing.Union\[.*?, NoneType\]$", str(type_)))


def is_typing_list(type_: typing.Any) -> bool:
    return issubclass(type_, List)


def is_typing_dict(type_: typing.Any) -> bool:
    return issubclass(type_, typing.Dict)


def join_not_none(iter_: typing.Iterable[typing.Optional[str]], sep: str = " ") -> str:
    return sep.join(filter(None, iter_))


def extract_field_type(field: Union[attr.Attribute, Type]) -> Type:
    type_ = field.type if isinstance(field, attr.Attribute) else field
    type_ = cast(Type, type_)

    if is_optional(type_):
        type_ = cast(Union[Type, Any], type_)
        type_ = type_.__args__[0]

    type_ = cast(Type, type_)
    return type_
