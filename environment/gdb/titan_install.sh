# !/bin/bash
#

cd /opt

wget http://s3.thinkaurelius.com/downloads/titan/titan-1.0.0-hadoop1.zip --show-progress
sudo unzip titan-1.0.0-hadoop1.zip 
sudo rm -f titan
sudo rm titan-1.0.0-hadoop1.zip
sudo ln -s /opt/titan-1.0.0-hadoop1/ /opt/titan

echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list 
curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add - 
sudo apt-get update 
sudo apt-get -y install cassandra 
#edit conf/gremlin-server/gremlin-server.yaml -> substitute "channelizer" line with: channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer

bin/titan.sh start
bin/gremlin.sh #test of the DB - Gremlin.version() or Titan.version() 
