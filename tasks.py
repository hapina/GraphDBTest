from invoke import task, run
import time
import os
import sys

GRAPH_DATABASES=['orientdb', 'neo4j'] 
CONF_DIR=os.path.dirname(os.path.realpath(__file__)) + '/config/'
CONF_DIR_ORIENTDB=os.path.dirname(os.path.realpath(__file__)) + '/config_orientdb/'

@task
def usage(ctx):
    """ Basic task information
    
        Example: invoke usage
    """
    print("\n\n  ***********************\n  *                     *\n  * GRAPH DATABASE TEST *\n  *                     *\n  *********************** \n\n")
    run('invoke -l')
    print ("For information about individual task use:\n\tinvoke --help <task>\n\nExample: invoke --help install\n")

@task
def clean(ctx):
    """ Clean environment
        - stop Gremlin server
        - drop data from graph databases
        - delete data from monitoring database
        
        Example: invoke clean
    """
    run('/opt/gremlin/bin/gremlin-server.sh stop && rm -rf /temp/gremlin_databases/ && rm -rf /opt/gremlin/ && cd graphdbtest && python3 cleanMonitoringDB.py')
    
@task
def install(ctx, database=None):
    """ Install graph database and prepare enviroment for testing
        - install graph database 
        - prepare and set database for testing
        - insert data about new graph database into monitoring
        
        Example: invoke install -d orientdb
    """
    if not database:
        run('invoke --help install')
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
        
    run('./environment/gdb/{db}_install.sh {ver}'.format(ver=version, db=database))
    run('cd graphdbtest && python3 insertgdb.py {db} {ver} "{des}"'.format(ver=version, db=database, des=description))

@task
def conf(ctx):
    """Check and store new configuration
        - check directory /config
        - set configuration
        - store new configuration into monitoring
        
        Example: invoke conf
    """
    configs = os.listdir(CONF_DIR)
    for conf in configs:
        run('cd graphdbtest && python3 insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=conf))
    
@task
def debug(ctx, experiment=None, database=None):
    """ Run experiment in debug mode
        Duplicity with invoke start, but you can see more information in terminal
        - both arguments are mandatory 
        - database: name of graph database 
        - experiment: experiment configuration file from directory /config
        
        Example: invoke debug -d orientdb -e e_select_001.conf
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
        
        Example: invoke start -d orientdb -e /e_select_001.conf
    """
    if not database or not experiment:
        error(101, "Not found mandatory arguments", "start")
    run('python3 graphdbtest/insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=experiment))
    runExperiment(ctx, database, experiment, False)
    
@task
def test(ctx, database=None):
    """ Caution: Run sequence of all test
        Run each defined experiment in /config directory in sequence mode for each installed database
        
        Example: invoke test
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
    """ Generate experiments stats to CSV file 
        You can generate all stats (without parameters) or you can choose from these options:
        - command - Stats relating to experiment type (select / import / create)
        - database - Stats relating to particular database (orientdb / titandb / arangodb)
        - experiment - Stats relating to particural experiment (ex_select_001.conf etc.)
        - query - Create your own report with using sql query. In this case other parameters will be ignored (except fileName). Notice the SQL command is used without semicolon bellow.
        
        Example: 
        invoke csv 
        invoke csv -f /path/report.csv
        invoke csv -d orientdb -e e_select_001.conf -c select
        invoke csv -q "select * from experiment" 
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
def png(ctx, command=None, database=None, experiment=None, query=None, fileName=None):
    """ Generate graph in PNG file 
        
        Example: invoke png
                 invoke png -f /path/fig.png
    """
    if not command:
        command = 'select'
    if not fileName:
        fileName = "/tmp/fig_{c}_{t}.png".format(t=time.strftime("%Y-%m-%d'T'%H:%M:%S"),c=command)
    options = params = ""
    if database:
        params += " -d {}".format(database) 
    if experiment:
        params += " -e {}".format(experiment)
    if query:
        params += ' -q "{}"'.format(query)
    run("cd graphdbtest && python3 {opts} genpng.py {par} -c {co} -f {fn}".format(opts=options, par=params, co=command, fn=fileName))
    
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

def error(errorCode=1, errorMessage=None, task=None):
    """ End task with error
    """
    if task:
        run('invoke --help {t}'.format(t=task))
    if errorMessage:
        print ("\n [ERR] " + str(errorCode) + ": " + errorMessage)
    exit(errorCode)
