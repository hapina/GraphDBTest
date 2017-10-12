# !/bin/bash
# from http://www.famvdploeg.com/blog/2013/01/setting-up-an-orientdb-server-on-ubuntu/
#


cd /opt

sudo wget https://bit.ly/orientdb-ce-imps-2-2-29-linux -O orientdb-community-2.2.29.zip
sudo tar -zxvf orientdb-community-2.2.29.zip 
sudo rm orientdb-community-2.2.29.zip 
sudo ln -s orientdb-community-importers-2.2.29/ orientdb
sudo vi orientdb/config/orientdb-server-config.xml

# <!-- Default in-memory storage. Data are not saved permanently. -->
# <storage path="memory:temp" name="temp" userName="yourUsername" userPassword="yourPassword" loaded-at-startup="true" />
# Get the root password for later use or/and add your own preferred account in [orient-server > users]:
# (I prefer to remove the root account and add a new one)

# <user name="yourUsername" password="yourPassword" resources="*"/>

# sudo chmod 640 /opt/orientdb/config/orientdb-server-config.xml
# useradd -d /opt/orientdb -M -r -s /bin/false -U orientdb
# chown -R orientdb.orientdb orientdb*
# sudo chmod 775 /opt/orientdb/bin
# sudo chmod g+x /opt/orientdb/bin/*.sh
# sudo usermod -a -G orientdb yourUsername

# sudo cp orientdb/bin/orientdb.sh /etc/init.d/
# sed -i "s|YOUR_ORIENTDB_INSTALLATION_PATH|/opt/orientdb|;s|USER_YOU_WANT_ORIENTDB_RUN_WITH|orientdb|" /etc/init.d/orientdb.sh

# You have to SET the OrientDB installation directory here (if not already done so)
ORIENTDB_DIR="/opt/orientdb"
ORIENTDB_USER="orientdb"
 
#su -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./server.sh 1>../log/orientdb.log 2>../log/orientdb.err &" - $ORIENTDB_USER
sudo -u $ORIENTDB_USER sh -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./server.sh 1>../log/orientdb.log 2>../log/orientdb.err &"
 
#su -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./shutdown.sh 1>>../log/orientdb.log 2>>../log/orientdb.err &" - $ORIENTDB_USER
sudo -u $ORIENTDB_USER sh -c "cd \"$ORIENTDB_DIR/bin\"; /usr/bin/nohup ./shutdown.sh 1>>../log/orientdb.log 2>>../log/orientdb.err &"

cd $ORIENTDB_DIR/bin
./server.sh

/opt/orientdb/bin/console.sh






