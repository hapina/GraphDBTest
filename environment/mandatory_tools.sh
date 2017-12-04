#!/bin/bash

#system check
apt-get -y update
apt-get -y upgrade

apt-get -y install sudo

#install python and its dependencies
apt-get -y install python3
apt-get -y install python3-pip

#python3 tools
pip3 install invoke
#pip3 install virtualenv

#java JDK
#apt-get -y install default-jdk

#git
#apt-get -y install git-core

#maven
#apt-get -y install maven

#virtualenv preparation
#virtualenv bulbs
#source bulbs/bin/activate

#Postgres installation
apt-get -y install postgresql postgresql-client
apt-get -y install libpq-dev

    
#instal OrientDB
#wget http://bit.ly/2qiDJ2a -O orientdb-community-3.0.0m2.tar.gz
#configure ORIENTDB_HOME/bin/orientdb.sh
#configure orientdb.service and copy to /etc/systemd/system/
#create orientdb user and group
#edit ORIENTDB_HOME/bin/server.sh memory value from ORIENTDB_OPTS_MEMORY="-Xms512m -Xmx512m" to ORIENTDB_OPTS_MEMORY="-Xms128m -Xmx256m"
