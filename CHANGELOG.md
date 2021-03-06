# Changelog

## Unreleased 

## [0.2.0](https://github.com/potykion/attrs_to_sql/tree/v0.2.0)

### Added 

- SqlAlchemy table > attrs

## [0.1.0](https://github.com/potykion/attrs_to_sql/tree/v0.1.0)

### Added 

- attrs_to_sqlalchemy_table: attrs > SqlAlchemy table

## [0.0.7](https://github.com/potykion/attrs_to_sql/tree/v0.0.7)

### Fixed

- `List[Dict]` as `json[]`

## [0.0.6](https://github.com/potykion/attrs_to_sql/tree/v0.0.6)

### Added

- `Dict` as `json` postgres type
- `IntEnum` as `int` type 

## [0.0.5](https://github.com/potykion/attrs_to_sql/tree/0.0.5)

### Added

- `Optional` type support
- Add imports to `__init__.py`
- Add _jinja2_ and _attrs_ to `install_requires`

### Fixed 

- Ignore `None` default
- Fix `List` type check on Python 3.7

## [0.0.4](https://github.com/potykion/attrs_to_sql/tree/0.0.4)

### Added

- `boolean` type support

### Fixed

- Move _templates_ dir to package
- Column name escaping

## [0.0.3](https://github.com/potykion/attrs_to_sql/tree/0.0.3)

### Fixed 

- Use class name as table name instead of fixed name

## [0.0.2](https://github.com/potykion/attrs_to_sql/tree/0.0.2)

### Fixed

- Convert `attrs_to_sql.py` to `attrs_to_sql` package

## [0.0.1](https://github.com/potykion/attrs_to_sql/tree/0.0.1)

### Added

- Convert `attrs` class to `CREATE TABLE` command
- SQL types support: `int`, `timestamp`, `varchar` (with length), `float`, arrays 
- SQL properties support: `PRIMARY KEY`, auto increment (via `serial`/`bigserial`), `NOT NULL`