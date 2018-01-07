# Graph Database Test 
Testing tool of graph databases.

## Prepare environment: 
 * `$ cd GraphDBTest` - all commands must be called from the main directory
 * `$ ./install.sh` - install environment

## Install and run graph database: 
Environment supports only selected graph databases, use help for more information.
* `$ invoke install --database <database>` - installation of a graph database
* `$ inv install -d <database>` - short version of the installation command above 
* `$ invoke --help install` - more info
#### Example:
* `$ inv install -d orientdb` - install OrientDB

#### Note: 
Read the logs, some databases can have its own requirements. For example way to start database server. 

## Prepare experiments configuration:
There are some experiments prepared for use. 

However you can modify them or even create whole new experiment sets.
All the configuration files for experiment setting must be placed in the `GraphDBTest/config/` directory. 
#### The mandatory parameters for any experiment are:
* `experiment_type` - can have these values: 
  * `select` - a gremlin query
  * `insert` - a gremlin insert command
  * `delete` - a gremlin delete command
  * `import` and `export` - import and export database using JSON 
  * `create` and `drop` - create and drop database
* `db_name` - database name, ie. `MovieDatabase`

## Run all experiments:
You can run all the experiments predefined in the `/config` directory with particular database or all of the databases that you have installed. 
* `$ invoke test --database <database>` or `$ inv test -d <database>`
* `$ invoke --help test` - more info
#### Example:
* `$ inv test` - for all databases
* `$ inv test -d orientdb` - will run the tests only for OrientDB

## Generate CSV file:
Generate reports about the testing to CSV file. You can modify the output of the report by adding more conditions or you can create your own report instead of the default one.
* `$ invoke csv --database <database> --experiment <experiment> --command <experiment_type> --fileName <file>` - default report with more conditions added
* `$ invoke csv --query <query> --fileName <file>` - your own report 
* `$ invoke --help csv` - more info
#### Example:
* `$ inv csv` - generate default report with timestamp based name
* `$ inv csv -q "select * from experiment" -f /path/report_OrientDB.csv` - generate your own report into the given directory
#### Note:
Notice that SQL command is used without the semicolon.

## Generate a charts to PNG file:
Generate interesting charts from the testing of the graph databases. You can generate all of them or choose the exact database, location or command type.
* `$ invoke png --database <database> --command <experiment_type> --fileName <file>` 
* `$ invoke --help png` - more info
#### Example:
* `$ inv png` - all default charts are generated to default location with timestamp based name
* `$ inv png -d orientdb -c select -f /path/fig.png` - generates chart with select type command used only for orientdb to defined filee 

## Run only one experiment and debug mode
If you want to run only one experiment defined in `/config` you can use `invoke --help start` for more info.
There is also debug mode - `invoke --help debug` for more info.

## Clean environment
* `$ invoke clean` 
* `$ invoke --help clean` - more info

## Help:
* `$ invoke usage`
