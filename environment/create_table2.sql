-- create tables
CREATE TABLE graphdb 
( gdb_id SERIAL PRIMARY KEY, gdb_name VARCHAR(20), gdb_desc VARCHAR(100), gdb_version VARCHAR(20));

CREATE TABLE measurement 
(meas_id SERIAL PRIMARY KEY, meas_name VARCHAR(20), meas_unit VARCHAR(20));

--CREATE TYPE request_type AS ENUM ('select', 'insert', 'create', 'delete', 'drop')

CREATE TABLE types 
(type_id SERIAL PRIMARY KEY, type_name VARCHAR(20), meas_id integer REFERENCES measurement(meas_id));

CREATE TABLE configuration 
(conf_id SERIAL PRIMARY KEY, conf_name VARCHAR(30), type_id integer REFERENCES types (type_id));

CREATE TABLE experiment 
(exper_id SERIAL PRIMARY KEY, run_date timestamp, iteration_count integer, gdb_id integer REFERENCES graphdb (gdb_id), conf_id integer REFERENCES configuration (conf_id));

CREATE TABLE iteration 
(iter_id SERIAL PRIMARY KEY, iter_timestamp timestamp, iter_number integer, status VARCHAR(10), exper_id integer REFERENCES experiment(exper_id));

CREATE TABLE measurement_value
(value_id SERIAL PRIMARY KEY, iter_id integer REFERENCES iteration (iter_id), meas_id integer REFERENCES measurement (meas_id), value NUMERIC(100,10));



INSERT TO TABLE graphdb (gdb_name, gdb_desc, gdb_version) VALUES ('orientdb', ...)
INSERT TO TABLE measurement (meas_name, meas_unit) VALUES ('run_time', ...)
INSERT TO TABLE configuration (conf_name, type_id) VALUES ('orientdb', ...)
INSERT TO TABLE types (type_name, meas_id) VALUES ('orientdb', ...)
