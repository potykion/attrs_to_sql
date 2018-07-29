from datetime import datetime
from typing import List, Optional, Dict, Any
import attr
from attrs_to_sql.table import attrs_to_table


@attr.s(auto_attribs=True)
class SampleModel:
    id: int = attr.ib(metadata={"primary_key": True, "type": "bigint", "auto_inc": True})
    title: str = attr.ib(metadata={"not_null": True, "length": 30})
    ids: list = attr.ib(metadata={"type": "bigint[]"})
    none_int: Optional[int] = None
    created_datetime: datetime = attr.ib(factory=datetime.now)
    ints: List[int] = attr.ib(factory=list)
    default_float: float = 2.5
    order: int = 1
    active: bool = False
    json_data: Dict = attr.ib(factory=dict)
    json_dict: dict = attr.ib(factory=dict)
    json_list: List[Dict] = attr.ib(factory=list)
    json_dict_with_type: Dict[str, Any] = attr.ib(factory=dict)


def test_attrs_to_table():
    with open("tests/data/model.sql", encoding="utf-8") as f:
        expected_sql = f.read()

    actual_sql = attrs_to_table(SampleModel)

    assert actual_sql == expected_sql
