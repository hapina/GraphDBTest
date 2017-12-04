#!/bin/bash

GraphDBTest_home=`pwd`
sudo -u postgres psql postgres -f psql_createUser.sql
sudo -u postgres psql postgres -c "drop database if exists experiment_monitoring"
sudo -u postgres psql postgres -f psql_createDatabase.sql
sudo -u postgres psql experiment_monitoring -f psql_createTable.sql
sudo -u postgres psql postgres -c "grant ALL on database experiment_monitoring to technical"
sudo -u postgres psql experiment_monitoring -c "grant ALL on table records to technical"
sudo -u postgres psql experiment_monitoring -c "grant ALL on table graph_databases to technical"
sudo -u postgres psql experiment_monitoring -c "grant ALL on table experiments_values to technical"
sudo -u postgres psql experiment_monitoring -c "grant ALL on table experiments_types to technical"
sudo -u postgres psql experiment_monitoring -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO technical"
sudo -u postgres psql experiment_monitoring -c "COPY experiments_values (value_name, exper_id) FROM '$GraphDBTest_home/exper_values.csv' CSV HEADER"
sudo -u postgres psql experiment_monitoring -c "COPY experiments_types (exper_name, exper_description, exper_config_file) FROM '$GraphDBTest_home/exper_types.csv' CSV HEADER"
sudo -u postgres psql experiment_monitoring -c "COPY graph_databases (gdb_name, gdb_description, gdb_version) FROM '$GraphDBTest_home/graph_databases.csv' CSV HEADER"
