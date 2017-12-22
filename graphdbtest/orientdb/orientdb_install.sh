# !/bin/bash
# from http://www.famvdploeg.com/blog/2013/01/setting-up-an-orientdb-server-on-ubuntu/
#


cd /opt

sudo wget https://bit.ly/orientdb-ce-imps-2-2-29-linux -O orientdb-community-2.2.29.zip
sudo tar -zxvf orientdb-community-2.2.29.zip 
sudo rm orientdb-community-2.2.29.zip 
sudo ln -s orientdb-community-importers-2.2.29/ orientdb

# sudo vi orientdb/config/orientdb-server-config.xml
# <!-- Default in-memory storage. Data are not saved permanently. -->
# <storage path="memory:temp" name="temp" userName="yourUsername" userPassword="yourPassword" loaded-at-startup="true" />
# Get the root password for later use or/and add your own preferred account in [orient-server > users]:
# (I prefer to remove the root account and add a new one)
# <user name="admin" password="admin" resources="*"/>
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

# You have to SET the OrientDB installation directory here (if not already done so)
#ORIENTDB_DIR="/opt/orientdb"
#ORIENTDB_USER="orientuser"
 
#su -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./server.sh 1>../log/orientdb.log 2>../log/orientdb.err &" - $ORIENTDB_USER
#sudo -u $ORIENTDB_USER sh -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./server.sh 1>../log/orientdb.log 2>../log/orientdb.err &"
 
#su -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./shutdown.sh 1>>../log/orientdb.log 2>>../log/orientdb.err &" - $ORIENTDB_USER
#sudo -u $ORIENTDB_USER sh -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./shutdown.sh 1>>../log/orientdb.log 2>>../log/orientdb.err &"







