CREATE TABLE GRAPH_DATABASES (
	gdb_id		    char(10) PRIMARY KEY,
	gdb_name		varchar(20),
	gdb_description	varchar(50),
	gdb_home varchar(50)
);
CREATE TABLE RECORDS (
	record_id		char(10) PRIMARY KEY,
	timestamp	    timestamp,
	exper_id	    char(10),
	gdb_id	        char(10),
	status	        varchar(50),
	repetition	    integer,
	exper_run_time  bigint,
	db_size_before  bigint,
	db_size_after   bigint
);
CREATE TABLE EXPERIMENTS_TYPES (
	exper_id		    char(10) PRIMARY KEY,
	exper_name		    varchar(20),
	exper_description	varchar(50),
	exper_config_file	varchar(50)
);
CREATE TABLE EXPERIMENTS_VALUES (
	value_id		    char(10) PRIMARY KEY,
	value_name		    varchar(20),
	exper_id	        char(10)
);
