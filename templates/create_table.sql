CREATE TABLE public.model
(
    {% for column in columns %}
    {{ column }}
    {% endfor %}
);