#!/bin/bash
#
#
#

#sudo apt-get install python3-dev
sudo apt-get install postgresql postgresql-client postgresql-client-common
sudo -i -u postgres
createuser admin -P --interactive
createuser technical -PSrd --interactive
createdb EXPERIMENT_MONITORING
#sudo apt-get install postgresql-server-dev


