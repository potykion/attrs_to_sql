from typing import Optional

import attr
import pytest

from attrs_to_sql.utils import camelcase_to_underscore, is_optional


@pytest.mark.parametrize(
    "camelcase, underscore",
    [("SampleModel", "sample_model"), ("Model", "model"), ("under_score", "under_score")],
)
def test_camelcase_to_underscore(camelcase, underscore):
    assert camelcase_to_underscore(camelcase) == underscore


@attr.s(auto_attribs=True)
class ClassWithOptional:
    optional: Optional[int] = 1


def test_is_optional():
    assert is_optional(attr.fields(ClassWithOptional).optional.type)
