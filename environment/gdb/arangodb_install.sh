#!/bin/bash

#echo arangodb3 arangodb3/password password root | debconf-set-selections
#echo arangodb3 arangodb3/password_again password root | debconf-set-selections

curl https://download.arangodb.com/arangodb33/Debian_9.0/Release.key | sudo apt-key add -
echo 'deb https://download.arangodb.com/arangodb33/Debian_9.0/ /' | sudo tee /etc/apt/sources.list.d/arangodb.list
sudo apt-get -y install apt-transport-https
sudo apt-get update
sudo apt-get -y install arangodb3=3.3.1
#sudo apt-get install arangodb3-dbg=3.3.1
