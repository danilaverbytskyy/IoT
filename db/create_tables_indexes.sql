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
