#!/bin/bash

# system check
apt-get -y update
apt-get -y upgrade

apt-get -y install sudo
apt-get -y install curl

# install python and its dependencies
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install python3-tk

# python3 tools
pip3 install invoke

# Postgres installation
apt-get -y install postgresql postgresql-client libpq-dev

