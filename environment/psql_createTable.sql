-- create tables
CREATE TABLE GRAPHDB ( 
    gdb_id SERIAL PRIMARY KEY, 
    gdb_name VARCHAR(20), 
    gdb_description VARCHAR(100), 
    gdb_version VARCHAR(20)
);

CREATE TABLE MEASUREMENT (
    meas_id SERIAL PRIMARY KEY, 
    meas_name VARCHAR(20), 
    meas_unit VARCHAR(20)
);

CREATE TABLE CONFIGURATION (
    conf_id SERIAL PRIMARY KEY, 
    conf_name VARCHAR(30)
);

CREATE TYPE REQUEST_TYPE AS ENUM ('select', 'insert', 'create', 'delete', 'drop');

CREATE TABLE TYPES (
    type_id SERIAL PRIMARY KEY, 
    type_name REQUEST_TYPE, 
    meas_id integer REFERENCES MEASUREMENT(meas_id),
    conf_id integer REFERENCES CONFIGURATION(conf_id)
);

CREATE TABLE EXPERIMENT (
    exper_id SERIAL PRIMARY KEY, 
    run_date timestamp, 
    iteration_count integer, 
    gdb_id integer REFERENCES GRAPHDB(gdb_id), 
    conf_id integer REFERENCES CONFIGURATION(conf_id)
);

CREATE TABLE ITERATION (
    iter_id SERIAL PRIMARY KEY, 
    iter_timestamp timestamp, 
    iter_number integer, 
    status VARCHAR(50), 
    exper_id integer REFERENCES EXPERIMENT(exper_id)
);

CREATE TABLE MEASUREMSENT_VALUE (
    value_id SERIAL PRIMARY KEY, 
    iter_id integer REFERENCES ITERATION(iter_id), 
    meas_id integer REFERENCES MEASUREMENT(meas_id), 
    value NUMERIC(100,10)
);

-- privileges on database connection
REVOKE CONNECT
ON DATABASE EXPERIMENT_MONITORING
FROM PUBLIC;

GRANT CONNECT
ON DATABASE EXPERIMENT_MONITORING 
TO technical;

REVOKE ALL
ON ALL TABLES IN SCHEMA public 
FROM PUBLIC;

GRANT ALL
ON ALL TABLES IN SCHEMA public 
TO technical;

GRANT USAGE, SELECT 
ON ALL SEQUENCES IN SCHEMA public 
TO technical;
