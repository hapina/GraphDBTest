#!/bin/bash

GraphDBTest_home=$(dirname $(readlink -f $0))

cd environment && ./mandatory_tools.sh && cd monitoring && ./prepare_database.sh && ./insert_table.sh

cd $GraphDBTest_home
pip3 install -r ./requirements.txt
