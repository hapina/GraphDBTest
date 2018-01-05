#!/bin/bash

GraphDBTest_home=$(dirname $(readlink -f $0))

cd $GraphDBTest_home/environment && ./mandatory_tools.sh && echo "[INFO] Mandatory tools - installed succeed " 
cd $GraphDBTest_home/environment/monitoring && ./prepare_database.sh && ./insert_table.sh && echo "[INFO] Prepared monitoring database - succeed " 
cd $GraphDBTest_home/environment/gdb && ./gremlin_install.sh && echo "[INFO] Gremlin-server - installed succeed " 

cd $GraphDBTest_home
pip3 install -r ./requirements.txt && echo "[INFO] Python3 libraries - installed succeed " 
