# !/bin/bash
#

GraphDBTest_home=$(dirname $(readlink -f $0))
cd /opt

#sudo wget https://bit.ly/orientdb-ce-imps-2-2-29-linux -O orientdb-community-2.2.29.zip
sudo tar -zxvf $GraphDBTest_home/downloads/orientdb-community-2.2.29.zip 
#sudo rm orientdb-community-2.2.29.zip 
sudo ln -s orientdb-community-importers-2.2.29/ orientdb

sudo sed -i "s/<storages>/<storages><storage path='memory:temp' name='temp' userName='admin' userPassword='admin' loaded-at-startup='true' \/>/" orientdb/config/orientdb-server-config.xml
sudo sed -i "s/<users>/<users><user name='orientuser' password='password' resources='*' \/>/" orientdb/config/orientdb-server-config.xml
#--------
# error "Cannot allocate memory"
# in /opt/orientdb/bin/server.sh to change ORIENTDB_OPTS_MEMORY="-Xms128m -Xmx256m"
#--------
sudo chmod 640 /opt/orientdb/config/orientdb-server-config.xml
sudo useradd -d /opt/orientdb -M -r -s /bin/false -U orientuser
sudo chown -R orientuser.orientuser /opt/orientdb*
sudo chmod 775 /opt/orientdb/bin
sudo chmod g+x /opt/orientdb/bin/*.sh
sudo usermod -a -G orientuser orientuser

sudo cp orientdb/bin/orientdb.sh /etc/init.d/
sudo sed -i "s|YOUR_ORIENTDB_INSTALLATION_PATH|/opt/orientdb|;s|USER_YOU_WANT_ORIENTDB_RUN_WITH|orientuser|" /etc/init.d/orientdb.sh

echo "DONE"
