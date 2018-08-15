from typing import Any

from jinja2 import Environment, PackageLoader, Template

env = Environment(
    loader=PackageLoader("attrs_to_sql", "templates"), lstrip_blocks=True, trim_blocks=True
)


def render(template_name: str, **kwargs: Any) -> str:
    template: Template = env.get_template(template_name)
    return template.render(**kwargs)
