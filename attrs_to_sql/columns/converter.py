import attr


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
