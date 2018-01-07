# Graph Database Test 

## Prepare environment: 
 * `$ cd GraphDBTest` - all commands call from main directory
 * `$ ./install.sh` - install environment

## Install and run graph database: 
Environment supports only some graph database, use help for more information.
* `$ invoke install --database <database>` - installation of a graph database
* `$ inv install -d <database>` - short version of the installation command above 
* `$ invoke --help install` - more info
#### Example:
* `$ inv install -d orientdb` - install OrientDB

#### Note: 
Read the logs, some database can have its own requirements. For example way to start database server. 

## Prepare experiments configuration:
There are some experiments prepared for use. 

However you can modify them or create new experiments.
All configuration file for setting experiment must be in `GraphDBTest/config/` directory. 
#### The mandatory parameters for all types of experiments are:
* `experiment_type` - can have these values: 
  * `select` - a gremlin query
  * `insert` - a gremlin insert command
  * `delete` - a gremlin delete command
  * `import` and `export` - import and export database using JSON 
  * `create` and `drop` - create and drop database
* `db_name` - database name `MovieDatabase`

## Run all experiments:
You can run all of experiments from `/config` directory with particular database or all of databases that you installed before. 
* `$ invoke test --database <database>` or `$ inv test -d <database>`
* `$ invoke --help test` - more info
#### Example:
* `$ inv test` - for all databases
* `$ inv test -d orientdb` - all tests only for OrientDB

## Generate CSV file:
Generate reports about testing to CSV file. There is prepared default report which you can modify adding more conditions or you can prepare your own report.   
* `$ invoke csv --database <database> --experiment <experiment> --command <experiment_type> --fileName <file>` - default report with more conditions
* `$ invoke csv --query <query> --fileName <file>` - your own report 
* `$ invoke --help csv` - more info
#### Example:
* `$ inv csv` - generate full default report to default fileName
* `$ inv csv -q "select * from experiment"` - generate your own report to default fileName
#### Note:
Notice the SQL command is used without semicolon.

## Generate a charts to PNG file:
Generate a interesting charts from testing of graph database. You can generate all default charts to default or choose what you want. 
* `$ invoke png --database <database> --command <experiment_type> --fileName <file>` 
* `$ invoke --help png` - more info
#### Example:
* `$ inv png` - all default charts generate to default fileName
* `$ inv png -d orientdb -c select -f /path/fig.png` - generate select chart only for orientdb to defined file 

## Run only one experiment and debug mode
If you want run olny one experiment defined in `config` you can use `invoke --help start` for more info.
There is also debug mode - `invoke --help debug` for more info.

## Clean environment
* `$ invoke clean` 
* `$ invoke --help clean` - more info

## Help:
* `$ invoke usage`
