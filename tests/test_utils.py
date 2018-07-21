from typing import Optional, List

import attr
import pytest

from attrs_to_sql.utils import camelcase_to_underscore, is_optional, is_typing_list


@pytest.mark.parametrize(
    "camelcase, underscore",
    [("SampleModel", "sample_model"), ("Model", "model"), ("under_score", "under_score")],
)
def test_camelcase_to_underscore(camelcase, underscore):
    assert camelcase_to_underscore(camelcase) == underscore


@attr.s(auto_attribs=True)
class ClassWithOptionalAndList:
    optional: Optional[int] = 1
    list: List[int] = []


def test_is_optional():
    assert is_optional(attr.fields(ClassWithOptionalAndList).optional.type)


def test_is_typing_list():
    assert is_typing_list(attr.fields(ClassWithOptionalAndList).list.type)
