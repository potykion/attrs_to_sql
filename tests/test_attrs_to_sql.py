import attr

from attrs_to_sql import attrs_to_table


@attr.s
class Model:
    id: int = attr.ib(metadata={"primary_key": True, "type": "bigint"})


def test_attrs_to_table():
    with open("tests/data/model.sql", encoding="utf-8") as f:
        create_table_sql = f.read()

    assert attrs_to_table(Model) == create_table_sql
