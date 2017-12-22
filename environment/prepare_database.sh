#!/bin/bash

sudo -u postgres psql postgres -f psql_createUser.sql
sudo -u postgres psql postgres -f psql_createDatabase.sql
sudo -u postgres psql experiment_monitoring -f psql_createTable.sql




