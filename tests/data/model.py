import sqlalchemy as sa

metadata = sa.MetaData()

sample_model = sa.Table(
    "sample_model", metadata,
    sa.Column("id", sa.Integer),
    sa.Column("title", sa.Unicode),
    sa.Column("ids", sa.ARRAY(sa.Integer)),
    sa.Column("none_int", sa.Integer),
    sa.Column("created_datetime", sa.DateTime),
    sa.Column("ints", sa.ARRAY(sa.Integer)),
    sa.Column("default_float", sa.Float),
    sa.Column("order", sa.Integer),
    sa.Column("active", sa.Boolean),
    sa.Column("json_data", sa.JSON),
    sa.Column("json_dict", sa.JSON),
    sa.Column("json_list", sa.ARRAY(sa.JSON)),
    sa.Column("json_dict_with_type", sa.JSON),
    sa.Column("enum_field", sa.Enum(SampleEnum)),
)