create table if not exists sensors_data (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP,
    epoch INT,
    mote_id SMALLINT CHECK ( mote_id between 1 and 55),
    temperature REAL CHECK ( temperature between -60 and 60),
    humidity REAL CHECK ( humidity between 0 and 100),
    light REAL,
    voltage REAL
);

SELECT
  pg_size_pretty(pg_relation_size('sensors_data'))        AS table_only,
  pg_size_pretty(pg_indexes_size('sensors_data'))         AS indexes,
  pg_size_pretty(pg_total_relation_size('sensors_data'))  AS total;