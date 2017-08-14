# !/bin/bash
#
# Priprava prostredi - pip, komunikace s databazemi 
#

# pip
sudo apt-get install python3-pip
python3 -m pip install -U pip

# psycopg2 - modul pro Postgress
python3 -m pip install psycopg2

# xlrd - komunikace s excelem
python3 -m pip install xlrd


# Struktura pro metadata
mkdir POSTGRES_METADATA


