# Changelog

## Unreleased 

## [0.0.3](https://github.com/potykion/attrs_to_sql/tree/0.0.3)

### Fixed 

- Use class name as table name instead of fixed name

## [0.0.2](https://github.com/potykion/attrs_to_sql/tree/0.0.2)

### Added

- Convert `attrs_to_sql.py` to `attrs_to_sql` package

## [0.0.1](https://github.com/potykion/attrs_to_sql/tree/0.0.1)

### Added

- Convert `attrs` class to `CREATE TABLE` command
- SQL types support: `int`, `timestamp`, `varchar` (with length), `float`, arrays 
- SQL properties support: `PRIMARY KEY`, auto increment (via `serial`/`bigserial`), `NOT NULL`