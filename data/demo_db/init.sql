-- Ask Your Database - demo schema (Pagila, PostgreSQL flavour)
-- Source: https://github.com/postgresql/samples/blob/main/scds-dvdrental/
-- License: PostgreSQL License (https://www.postgresql.org/about/usage/)
-- This is a reduced subset of the Pagila DVD-rental sample database.
--
-- Tables:
--   category      - film categories (e.g. Action, Comedy)
--   film          - the movie catalogue
--   film_category - many-to-many film <-> category
--   actor         - people who act in films
--   film_actor    - many-to-many film <-> actor
--   customer      - rental customers
--   address       - customer addresses
--   city          - cities
--   country       - countries
--   store         - physical rental stores
--   staff         - store employees
--   inventory     - physical copies of each film held at a store
--   rental        - each rental transaction
--   payment        - each payment transaction for a rental

BEGIN;

CREATE TABLE IF NOT EXISTS country (
    country_id   smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country      varchar(50) NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS city (
    city_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city         varchar(50) NOT NULL,
    country_id   smallint NOT NULL REFERENCES country (country_id),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS address (
    address_id   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    address      varchar(50),
    address2     varchar(50),
    district     varchar(20),
    city_id      smallint NOT NULL REFERENCES city (city_id),
    postal_code  varchar(10),
    phone        varchar(20),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS customer (
    customer_id  integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id     smallint NOT NULL,
    first_name   varchar(45) NOT NULL,
    last_name    varchar(45) NOT NULL,
    email        varchar(50),
    address_id   smallint NOT NULL REFERENCES address (address_id),
    active       boolean NOT NULL DEFAULT true,
    create_date  timestamp NOT NULL DEFAULT now(),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS language (
    language_id  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         varchar(20) NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS category (
    category_id  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         varchar(25) NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS film (
    film_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        varchar(255) NOT NULL,
    description  text,
    release_year  integer,
    language_id  smallint NOT NULL REFERENCES language (language_id),
    original_language_id smallint REFERENCES language (language_id),
    rental_rate  numeric(3,2) NOT NULL DEFAULT 4.99,
    length       smallint,
    rating       varchar(5),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS film_category (
    film_id      integer NOT NULL REFERENCES film (film_id),
    category_id  smallint NOT NULL REFERENCES category (category_id),
    last_update  timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (film_id, category_id)
);

CREATE TABLE IF NOT EXISTS actor (
    actor_id     smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name   varchar(45) NOT NULL,
    last_name    varchar(45) NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS film_actor (
    actor_id     smallint NOT NULL REFERENCES actor (actor_id),
    film_id      integer NOT NULL REFERENCES film (film_id),
    last_update  timestamp NOT NULL DEFAULT now(),
    PRIMARY KEY (actor_id, film_id)
);

CREATE TABLE IF NOT EXISTS store (
    store_id     smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    manager_staff_id integer,
    address_id   smallint NOT NULL REFERENCES address (address_id),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id     smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name   varchar(45) NOT NULL,
    last_name    varchar(45) NOT NULL,
    address_id   smallint NOT NULL REFERENCES address (address_id),
    email        varchar(50),
    store_id     smallint NOT NULL,
    active       boolean NOT NULL DEFAULT true,
    username     varchar(16) NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

ALTER TABLE store ADD CONSTRAINT store_manager_staff_id_fkey
    FOREIGN KEY (manager_staff_id) REFERENCES staff (staff_id);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    film_id      integer NOT NULL REFERENCES film (film_id),
    store_id     smallint NOT NULL REFERENCES store (store_id),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rental (
    rental_id    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rental_date  timestamp NOT NULL,
    inventory_id integer NOT NULL REFERENCES inventory (inventory_id),
    customer_id  integer NOT NULL REFERENCES customer (customer_id),
    return_date  timestamp,
    staff_id     integer NOT NULL REFERENCES staff (staff_id),
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id  integer NOT NULL REFERENCES customer (customer_id),
    rental_id    integer NOT NULL REFERENCES rental (rental_id),
    amount       numeric(5,2) NOT NULL,
    payment_date timestamp NOT NULL,
    last_update  timestamp NOT NULL DEFAULT now()
);

CREATE INDEX idx_film_category_category_id ON film_category (category_id);
CREATE INDEX idx_film_actor_actor_id ON film_actor (actor_id);
CREATE INDEX idx_rental_inventory_id ON rental (inventory_id);
CREATE INDEX idx_rental_customer_id ON rental (customer_id);
CREATE INDEX idx_rental_staff_id ON rental (staff_id);
CREATE INDEX idx_payment_customer_id ON payment (customer_id);
CREATE INDEX idx_payment_rental_id ON payment (rental_id);
CREATE INDEX idx_inventory_film_id ON inventory (film_id);
CREATE INDEX idx_inventory_store_id ON inventory (store_id);
CREATE INDEX idx_customer_store_id ON customer (store_id);
CREATE INDEX idx_customer_address_id ON customer (address_id);
CREATE INDEX idx_address_city_id ON address (city_id);
CREATE INDEX idx_city_country_id ON city (country_id);

COMMIT;