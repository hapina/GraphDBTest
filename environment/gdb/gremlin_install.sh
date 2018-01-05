# !/bin/bash
#

GraphDBTest_home=$(dirname $(readlink -f $0))
cd /opt

cp -r $GraphDBTest_home/downloads/apache-tinkerpop-gremlin-server-3.3.1 .
sudo ln -sf /opt/apache-tinkerpop-gremlin-server-3.3.1/ /opt/gremlin

