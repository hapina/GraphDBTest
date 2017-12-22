#!/bin/bash

GraphDBTest_home=$(dirname $(readlink -f $0))
echo $GraphDBTest_home

# initial insert for static table 
sudo -u postgres psql experiment_monitoring -c "COPY MEASUREMENT FROM '$GraphDBTest_home/metadata/measurement.csv' CSV HEADER"
sudo -u postgres psql experiment_monitoring -c "COPY CONFIGURATION FROM '$GraphDBTest_home/metadata/configuration.csv' CSV HEADER"
sudo -u postgres psql experiment_monitoring -c "COPY TYPES FROM '$GraphDBTest_home/metadata/types.csv' CSV HEADER"

