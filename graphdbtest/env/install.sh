#!/bin/bash
#
# Priprava prostredi - pip, komunikace s databazemi 
# 


#system update
apt-get update
apt-get upgrade

#python installation
apt-get install python3
apt-get install python3-pip

# git
apt-get install git

#python tools
pip3 install invoke

# virtualenv
pip3 install virtualenv

# java
apt-get install default-jdk

# $JAVA_HOME

# mvn
# !!! get maven zip
echo $JAVA_HOME
unzip apache-maven-3.5.2-bin.zip
export PATH=/opt/apache-maven-3.5.2/bin:$PATH
mvn -v 

# bulbs
mkdir example
cd example
virtualenv env
source env/bin/activate # env is activate - (env)$ 
pip install bulbs
deactivate # deactivate env

# rexter
git clone https://github.com/tinkerpop/rexster.git
cd rexster
mvn clean install

# gremlin
git clone https://github.com/tinkerpop/gremlin.git
cd gremlin
mvn clean install

# psycopg2 - modul pro Postgress
# python3 -m pip install psycopg2

# xlrd - komunikace s excelem
# python3 -m pip install xlrd

# Struktura pro metadata
# mkdir POSTGRES_METADATA



