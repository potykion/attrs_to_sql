@attr.s(auto_attribs=True)
class Entity:
    id: int
    title: str
    address: Dict
    active: bool
    emails: List[str]
