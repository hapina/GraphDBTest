CREATE TABLE databases_types (
	db_id		 char(10) PRIMARY KEY,
	db_name		 varchar(20),
	db_description	 varchar(50),
	db_configuration varchar(50),
	db_gremlin	 boolean,
	db_blueprint	 boolean,
	db_java		 boolean
);
CREATE TABLE experiments_records (
	r_id		char(10) PRIMARY KEY,
	r_timestamp	timestamp,
	r_experiment_id	char(10),
	r_database_id	char(10),
	r_repetition	integer,
	r_status	varchar(50)
);
CREATE TABLE experiments_types (
	e_id		char(10) PRIMARY KEY,
	e_name		varchar(20),
	e_description	varchar(50),
	e_configuration	varchar(50),
	e_type		varchar(10)
);
