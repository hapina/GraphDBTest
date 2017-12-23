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
pip3 install python3-seaborn

#java JDK
#apt-get -y install default-jdk

#git
#apt-get -y install git-core

#Postgres installation
apt-get -y install postgresql postgresql-client
#apt-get -y install libpq-dev


