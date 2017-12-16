#!/bin/bash


cd environment && ./mandatory_tools.sh && ./prepare_database.sh
python3 -m pip install -r REQUIREMENTS
