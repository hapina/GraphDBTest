-- create tables
CREATE TABLE GRAPHDB ( 
    gdb_id SERIAL PRIMARY KEY, 
    gdb_name VARCHAR(20) UNIQUE, 
    gdb_description VARCHAR(100), 
    gdb_version VARCHAR(20)
);
SELECT SETVAL('graphdb_gdb_id_seq',1);

CREATE TABLE MEASUREMENT (
    meas_id SERIAL PRIMARY KEY, 
    meas_name VARCHAR(20) UNIQUE, 
    meas_unit VARCHAR(20)
);
SELECT SETVAL('measurement_meas_id_seq',1);

CREATE TABLE CONFIGURATION (
    conf_id SERIAL PRIMARY KEY, 
    conf_name VARCHAR(30) UNIQUE
);
SELECT SETVAL('configuration_conf_id_seq',1);

CREATE TYPE REQUEST_TYPE AS ENUM ('select', 'insert', 'create', 'delete', 'drop', 'import', 'export');

CREATE TABLE TYPES (
    type_id SERIAL PRIMARY KEY, 
    type_name REQUEST_TYPE, 
    meas_id integer REFERENCES MEASUREMENT(meas_id),
    conf_id integer REFERENCES CONFIGURATION(conf_id)
);
SELECT SETVAL('types_type_id_seq',1);

CREATE TABLE EXPERIMENT (
    exper_id SERIAL PRIMARY KEY, 
    run_date timestamp, 
    iteration_count integer, 
    gdb_id integer REFERENCES GRAPHDB(gdb_id), 
    conf_id integer REFERENCES CONFIGURATION(conf_id)
);
SELECT SETVAL('experiment_exper_id_seq',1);

CREATE TABLE ITERATION (
    iter_id SERIAL PRIMARY KEY, 
    iter_timestamp timestamp, 
    iter_number integer, 
    status VARCHAR(50), 
    exper_id integer REFERENCES EXPERIMENT(exper_id)
);
SELECT SETVAL('iteration_iter_id_seq',1);

CREATE TABLE MEASUREMENT_VALUE (
    value_id SERIAL PRIMARY KEY, 
    iter_id integer REFERENCES ITERATION(iter_id), 
    meas_id integer REFERENCES MEASUREMENT(meas_id), 
    value NUMERIC(100,10)
);
SELECT SETVAL('measurement_value_value_id_seq',1);

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
