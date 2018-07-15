CREATE TABLE public.sample_model
(
    id bigserial PRIMARY KEY,
    title varchar(30) NOT NULL,
    ids bigint[],
    default_int int DEFAULT 1,
    created_datetime timestamp,
    ints int[],
    default_float float DEFAULT 2.5
);