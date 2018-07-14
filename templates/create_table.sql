CREATE TABLE public.model
(
    {% for column in columns %}
    {{ column }}{% if not loop.last %},{% endif %}

    {% endfor %}
);