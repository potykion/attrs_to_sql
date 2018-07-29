CREATE TABLE public.sample_model
(
    "id" bigserial PRIMARY KEY,
    "title" varchar(30) NOT NULL,
    "ids" bigint[],
    "none_int" int,
    "created_datetime" timestamp,
    "ints" int[],
    "default_float" float DEFAULT 2.5,
    "order" int DEFAULT 1,
    "active" boolean DEFAULT FALSE,
    "json_data" json,
    "json_dict" json,
    "json_list" json,
    "json_dict_with_type" json
);