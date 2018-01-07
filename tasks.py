from invoke import task, run
import time
import os
import sys

GRAPH_DATABASES=['orientdb', 'neo4j'] 
TYPE_EXPERIMENT=['select', 'insert', 'import', 'create']
DIR=os.path.dirname(os.path.realpath(__file__))
CONF_DIR='{}/config/'.format(DIR)
CONF_DIR_ORIENTDB='{}/config_orientdb/'.format(DIR)
    
@task
def usage(ctx):
    """ Basic task information
    
        Example: invoke usage
    """
    print("\n  ***********************\n  *                     *\n  * GRAPH DATABASE TEST *\n  *                     *\n  *********************** \n")
    run('invoke -l')
    print ("For information about individual task use:\n\tinvoke --help <task>\n\nExample: invoke --help install\n")

@task
def clean(ctx):
    """ Clean environment
        - stop Gremlin server
        - drop data from graph databases
        - delete data from monitoring database
        
        Example: 
        inv clean
    """
    run('/opt/gremlin/bin/gremlin-server.sh stop && rm -rf /temp/gremlin_databases/ && rm -rf /opt/gremlin/ && cd graphdbtest && python3 cleanMonitoringDB.py')
    
@task
def install(ctx, database=None):
    """ Install graph database and prepare enviroment for testing
        - install graph database 
        - prepare and set database for testing
        - insert data about new graph database into monitoring 
        
        For supported database use only - invoke install 
        
        Example: 
        inv install -d orientdb
    """
    if database == 'orientdb':    
        description = 'OrientDB, document-graph database'
        version = 'v2.2' #'2.4.0' 
    elif database == 'sparksee':    
        description = 'Sparksee, high-performance graph database'
        version = '2.6.0'
    elif database == 'bitsy':    
        description = 'Bitsy, small and fast in-memory graph database'
        version = '1.5.2'
    elif database == 'neo4j':    
        description = 'Neo4j, the internet-scale graph platform'
        version = '3.3.1'
    elif database == 'tinkergraph':    
        description = 'TinkerGraph, lightweight in-memory property graph'
        version = '2.6.0'
    elif database == 'arangodb':    
        description = 'Arango DB, native multi-model database'
        version = 'v3.3'
    else:
        print("WARN: Unsupported database: {db} \n\t You can use this databases {mygdb}".format(db=database, mygdb=GRAPH_DATABASES))
        error()
        
    run('cd graphdbtest && python3 insertgdb.py {db} {ver} "{des}"'.format(ver=version, db=database, des=description))
    run('{dir}/environment/gdb/{db}_install.sh {ver}'.format(dir=DIR,ver=version, db=database))

    
@task
def debug(ctx, experiment=None, database=None):
    """ Run experiment in debug mode
        Duplicity with invoke start, but you can see more information in terminal
        - both arguments are mandatory 
        - database: name of graph database 
        - experiment: experiment configuration file from directory /config
        
        Example: 
        inv debug -d orientdb -e e_select_001.conf
    """
    if not database or not experiment:
        error(101, "Not found mandatory arguments", "debug")
    run('python3 graphdbtest/insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=experiment))
    runExperiment(ctx, database, experiment)
    
@task
def start(ctx, experiment=None, database=None):
    """ Run graph database experiment
        - both arguments are mandatory 
        - database: name of graph database 
        - experiment: experiment configuration file from directory /config
        
        Example: 
        inv start -d orientdb -e /e_select_001.conf
    """
    if not database or not experiment:
        error(101, "Not found mandatory arguments", "start")
    run('python3 graphdbtest/insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=experiment))
    runExperiment(ctx, database, experiment, False)
    
@task
def test(ctx, database=None):
    """ Caution: Run sequence of all test, it can take some time.
        Run each defined experiment in /config directory in sequence mode for each installed database or one defined database.
        
        Example: 
        inv test
        inv test -d orientdb
        
        NOTE: For OrientDB is used extra /config_orientdb directory because OrientDB using another variant of Gremlin! If you modify /config , you must modify /config_orientdb similary for comparing with another databases.
    """
    print("INFO: Configuration checking")
    conf(ctx)
    print("INFO: RUN TESTING")
    if database:
        if database in GRAPH_DATABASES:
            databases = [database]
        else:
            print("WARN: Unsupported database: {db} \n\t You can use this databases {mygdb}".format(db=database, mygdb=GRAPH_DATABASES))
            error()
    else:
        databases = GRAPH_DATABASES
    i=0
    configs = sorted(os.listdir(CONF_DIR))
    for db in databases:
        for cf in configs:
            i+=1
            print("INFO: Test no. {i}, {db}, {cf}".format(i=i,db=db,cf=cf))
            start(ctx, cf, db)
            
@task
def csv(ctx, command=None, database=None, experiment=None, fileName=None, query=None):
    """ Generate reports about testing to CSV file. 
        There is prepared default report which you can modify adding more conditions or you can prepare your own report.
    
        For adding more confitions or create own reports:
        - command - Stats relating to experiment type (select / import / create)
        - database - Stats relating to particular database (orientdb / titandb / arangodb)
        - experiment - Stats relating to particural experiment (ex_select_001.conf etc.)
        - query - Create your own report with using sql query. In this case other parameters will be ignored (except fileName). Notice the SQL command is used without semicolon bellow.
        
        Example: 
        inv csv 
        inv csv -f /path/report.csv
        inv csv -d orientdb -e e_select_001.conf -c select
        inv csv -q "select * from experiment" 
    """
    if not fileName:
        fileName = "/tmp/report_{}.csv".format(time.strftime("%Y-%m-%d'T'%H:%M:%S"))
    options = params = ""

    if command:
        params += " -c {}".format(command)
    if database:
        params += " -d {}".format(database) 
    if experiment:
        params += " -e {}".format(experiment)
    if query:
        params += ' -q "{}"'.format(query)
    run("cd graphdbtest && python3 {opts} gencsv.py {par} -f {fn}".format(opts=options, par=params, fn=fileName))
        
@task
def png(ctx, command=None, database=None, fileName=None):
    """ Generate a interesting charts from testing of graph database. 
        You can generate all default charts to default or choose what you want.  
        
        Example: 
        inv png - all default charts generate to default fileName
        inv png -d orientdb -c select -f /path/fig.png` - generate select chart only for orientdb to defined file 
    """
    if command:
        commands = [command]
    else:
        commands = TYPE_EXPERIMENT
    options = params = ""
    if database:
        params += " -d {}".format(database) 
    
    for com in commands:
        if fileName:
            fn = fileName
        else:
            fn = "/tmp/fig_{c}_{t}.png".format(t=time.strftime("%Y-%m-%d'T'%H:%M:%S"),c=com)
        run("cd graphdbtest && python3 {opts} genpng.py {par} -c {co} -f {fn}".format(opts=options, par=params, co=com, fn=fn))
    
def runExperiment(ctx, db=None, ex=None, debug=True):
    """ Starts the experiment for the set database 
    """
    options=""
    if not debug:
        options += "-O"
    if db == 'orientdb':
        confDir = CONF_DIR_ORIENTDB
    else:
        confDir = CONF_DIR
    run('cd graphdbtest && python3 {opts} runtest.py -d {db} -e {ex}'.format(opts=options, db=db, ex=confDir+ex) )    

def conf(ctx):
    """Check and store new configuration
        - check directory /config
        - set configuration
        - store new configuration into monitoring
    """
    configs = os.listdir(CONF_DIR)
    for conf in configs:
        run('cd graphdbtest && python3 insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=conf))

def error(errorCode=1, errorMessage=None, task=None):
    """ End task with error
    """
    if task:
        run('invoke --help {t}'.format(t=task))
    if errorMessage:
        print ("\n [ERR] " + str(errorCode) + ": " + errorMessage)
    exit(errorCode)
