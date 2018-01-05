from invoke import task, run
import time
import os
import sys

GRAPH_DATABASES=['orientdb','tinkergraph', 'bitsy', 'neo4j', 'arangodb'] 
CONF_DIR=os.path.dirname(os.path.realpath(__file__)) + '/config/'

@task
def usage(ctx):
    """ Basic task information
    
        Example: invoke usage
    """
    print("\n\n  ***********************\n  *                     *\n  * GRAPH DATABASE TEST *\n  *                     *\n  *********************** \n\n")
    run('invoke -l')
    print ("For information about individual task use:\n\tinvoke --help <task>\n\nExample: invoke --help install\n")

@task
def install(ctx, database=None, version=None):
    """ Install graph database and prepare enviroment for testing
        - install graph database 
        - prepare and set database for testing
        - insert data about new graph database into monitoring
        
        Example: invoke install -d orientdb
    """
    if not database:
        run('invoke --help install')
    if database == 'orientdb':    
        print("INFO: Install OrientDB")
        if not version:
            version = 'v2.2'
        run('./environment/gdb/orientdb_install.sh {ver} && cd graphdbtest && python3 insertgdb.py orientdb {ver}'.format(ver=version))
    elif database == 'tinkergraph':    
        print("INFO: Install TinkerGraph")
        if not version:
            version = 'v3.2'
        #run('./environment/gdb/gremlin_install.sh {ver} && cd graphdbtest && python3 insertgdb.py tinkergraph {ver}'.format(ver=version))
    elif database == 'bitsy':    
        print("INFO: Install Bitsy")
        if not version:
            version = 'v??'
        #run('./environment/gdb/arangodb_install.sh {ver} && cd graphdbtest && python3 insertgdb.py arangodb {ver}'.format(ver=version))
    elif database == 'neo4j':    
        print("INFO: Install Neo4j")
        if not version:
            version = 'v??'
        #run('./environment/gdb/arangodb_install.sh {ver} && cd graphdbtest && python3 insertgdb.py arangodb {ver}'.format(ver=version))
    elif database == 'arangodb':    
        print("INFO: Install ArangoDB")
        if not version:
            version = 'v3.3'
        #run('./environment/gdb/arangodb_install.sh {ver} && cd graphdbtest && python3 insertgdb.py arangodb {ver}'.format(ver=version))
    else:
        print("WARN: Bad parameter database: {db} \n\t You can use this databases {mygdb}".format(db=database, mygdb=GRAPH_DATABASES))

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
def debug(ctx, experimentConfig=None, graphDatabaseName=None):
    """ Run experiment in debug mode
        Duplicity with invoke start, but you can see more information in terminal
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file from directory /config
        
        Example: invoke debug -d orientdb -e /e_select_001.conf
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "debug")
    run('python3 graphdbtest/insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=experimentConfig))
    runExperiment(ctx, graphDatabaseName, experimentConfig)
    
@task
def start(ctx, experimentConfig=None, graphDatabaseName=None):
    """ Run graph database experiment
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file from directory /config
        
        Example: invoke start -d orientdb -e /e_select_001.conf
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "start")
    run('python3 graphdbtest/insertConf.py {dir} {conf}'.format(dir=CONF_DIR,conf=experimentConfig))
    runExperiment(ctx, graphDatabaseName, experimentConfig, False)
    
@task
def test(ctx, database=None):
    """ Caution: Run sequence of all test
        Run each defined experiment in /config directory in sequence mode for each installed database
        
        Example: invoke test
    """
    print("INFO: Configuration checking")
    conf(ctx)
    print("INFO: RUN TESTING")
    configs = sorted(os.listdir(CONF_DIR))
    if database:
        databases = [database]
    else:
        databases = GRAPH_DATABASES
    i=0
    for cf in configs:
        for db in databases:
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
def png(ctx, command=None, database=None, experiment=None, fileName=None, query=None):
    """ Generate graph in PNG file 
        
        Example: invoke png
                 invoke png -f /path/fig.png
    """
    if not fileName:
        fileName = "/tmp/fig_{}.png".format(time.strftime("%Y-%m-%d'T'%H:%M:%S"))
    options = params = ""

    if command:
        params += " -c {}".format(command)
    if database:
        params += " -d {}".format(database) 
    if experiment:
        params += " -e {}".format(experiment)
    if query:
        params += ' -q "{}"'.format(query)
    run("cd graphdbtest && python3 {opts} genpng.py {par} -f {fn}".format(opts=options, par=params, fn=fileName))
    
def runExperiment(ctx, db=None, ex=None, debug=True):
    """ Starts the experiment for the set database 
    """
    options=""
    if not debug:
        options += "-O"
    run('cd graphdbtest && python3 {opts} runtest.py -d {db} -e {ex}'.format(opts=options, db=db, ex=CONF_DIR+ex) )    

def error(errorCode=1, errorMessage=None, task=None):
    """ End task with error
    """
    if task:
        run('invoke --help {t}'.format(t=task))
    if errorMessage:
        print ("\n [ERR] " + str(errorCode) + ": " + errorMessage)
    exit(errorCode)
