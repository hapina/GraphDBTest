CREATE TABLE graph_databases (
	gdb_id		    SERIAL PRIMARY KEY,
	gdb_name		varchar(20) NOT NULL,
	gdb_description	varchar(100),
	gdb_version     varchar(20)
);
CREATE TABLE records (
	record_id		BIGSERIAL PRIMARY KEY,
	timestamp	    timestamp NOT NULL,
	exper_id	    integer,
	gdb_id	        integer,
	status	        varchar(50) NOT NULL,
	repetition	    integer,
	run_time        double precision,
	size_before     double precision,
	size_after      double precision
);
CREATE TABLE experiments_types (
	exper_id		    SERIAL PRIMARY KEY,
	exper_name		    varchar(20) NOT NULL,
	exper_description	varchar(100),
	exper_config_file	varchar(50)
);
CREATE TABLE experiments_values (
	value_id		    SERIAL PRIMARY KEY,
	value_name		    varchar(20) NOT NULL,
	exper_id	        integer NOT NULL
);
