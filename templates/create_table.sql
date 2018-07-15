CREATE TABLE public.{{ table }}
(
    {% for column in columns %}
    {{ column }}{% if not loop.last %},{% endif %}

    {% endfor %}
);