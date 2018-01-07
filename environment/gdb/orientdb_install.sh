# !/bin/bash
#

GraphDBTest_home=$(dirname $(readlink -f $0))
Version=$1

cd /opt

# verze 2.2.31, unstable 3.0.0RC1
[[ $Version == v2.2 ]] && sudo tar -zxvf $GraphDBTest_home/downloads/orientdb-community-2.2.31.zip  
[[ $Version == v3.0 ]] && sudo tar -zxvf $GraphDBTest_home/downloads/orientdb-community-importers-3.0.0RC1.tar.gz  
sudo rm -f orientdb
[[ $Version == v2.2 ]] && sudo ln -s /opt/orientdb-community-importers-2.2.31/ /opt/orientdb
[[ $Version == v3.0 ]] && sudo ln -s /opt/orientdb-community-importers-3.0.0RC1/ /opt/orientdb


sudo sed -i "s/<storages>/<storages><storage path='memory:temp' name='temp' userName='admin' userPassword='admin' loaded-at-startup='true' \/>/" /opt/orientdb/config/orientdb-server-config.xml
sudo sed -i "s/<users>/<users><user name='orientuser' password='password' resources='*' \/>/" /opt/orientdb/config/orientdb-server-config.xml
sudo sed -i "s/ORIENTDB_OPTS_MEMORY=\"-Xms2G -Xmx2G/ORIENTDB_OPTS_MEMORY=\"-Xms128m -Xmx256m/" /opt/orientdb/bin/server.sh

sudo chmod 640 /opt/orientdb/config/orientdb-server-config.xml
sudo useradd -d /opt/orientdb -M -r -s /bin/false -U orientuser
sudo chown -R orientuser.orientuser /opt/orientdb*
sudo chmod 775 /opt/orientdb/bin
sudo chmod g+x /opt/orientdb/bin/*.sh
sudo usermod -a -G orientuser orientuser

#sudo cp orientdb/bin/orientdb.sh /etc/init.d/
#sudo sed -i "s|YOUR_ORIENTDB_INSTALLATION_PATH|/opt/orientdb|;s|USER_YOU_WANT_ORIENTDB_RUN_WITH|orientuser|" /etc/init.d/orientdb.sh

#cat<<<"[INFO] For start server use $GraphDBTest_home/orientdb_server.sh start"
$GraphDBTest_home/orientdb_server.sh start &

