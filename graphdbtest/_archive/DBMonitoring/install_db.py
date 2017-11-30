#!/bin/bash
#
#
#

#sudo apt-get install python3-dev
groupadd database
useradd -G database,sudo techuser
# id techuser
sudo apt-get install postgresql postgresql-client postgresql-client-common
sudo -i -u postgres
createuser hapina -P --interactive
createuser techuser -PSrd --interactive
createdb EXPERIMENT_MONITORING
#sudo apt-get install postgresql-server-dev


