from datetime import datetime
import attr
from attrs_to_sql import attrs_to_table


@attr.s(auto_attribs=True)
class Model:
    id: int = attr.ib(metadata={"primary_key": True, "type": "bigint", "auto_inc": True})
    default_int: int = 1
    created_datetime: datetime = attr.ib(factory=datetime.now)


def test_attrs_to_table():
    with open("tests/data/model.sql", encoding="utf-8") as f:
        expected_sql = f.read()

    actual_sql = attrs_to_table(Model)

    assert actual_sql == expected_sql
