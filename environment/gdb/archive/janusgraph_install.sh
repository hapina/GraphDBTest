# !/bin/bash
#

GraphDBTest_home=$(dirname $(readlink -f $0))
echo $GraphDBTest_home
#wget https://github.com/JanusGraph/janusgraph/releases/download/v0.2.0/janusgraph-0.2.0-hadoop2.zip --show-progress
#sudo unzip janusgraph-0.2.0-hadoop2.zip
#sudo rm janusgraph-0.2.0-hadoop2.zip

cp -r $GraphDBTest_home/downloads/janusgraph-0.2.0-hadoop2/ /opt/
cd /opt
sudo ln -sf /opt/janusgraph-0.2.0-hadoop2/ /opt/janusgraph

#echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list 
#curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add - 
#sudo apt-get update 
#sudo apt-get -y install cassandra 
#edit conf/gremlin-server/gremlin-server.yaml -> substitute "channelizer" line with: channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer

cd janusgraph
bin/janusgraph.sh start
#bin/gremlin.sh #test of the DB - Gremlin.version() or Titan.version() 
