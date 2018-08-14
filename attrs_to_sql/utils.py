import re
import typing


def camelcase_to_underscore(camelcase: str) -> str:
    """https://stackoverflow.com/a/1176023"""
    underscored = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camelcase)
    underscored = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", underscored)
    lowered = underscored.lower()
    return lowered


def is_optional(type_: typing.Any) -> bool:
    return bool(re.match(r"^typing.Union\[.*?, NoneType\]$", str(type_)))


def is_typing_list(type_: typing.Any) -> bool:
    type_str = str(type_)
    return type_str.startswith("typing.List") or type_str.startswith("list")


def is_typing_dict(type_: typing.Any) -> bool:
    type_str = str(type_)
    return type_str.startswith("typing.Dict") or type_str.startswith("dict")


def join_not_none(iter_: typing.Iterable[typing.Optional[str]], sep: str = " "):
    return sep.join(filter(None, iter_))
