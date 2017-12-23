from invoke import task, run
import time
import os
import sys

REQUIREMENTS='requirements.txt'
GRAPH_DATABASES=['orientdb', 'arangodb']

@task
def usage(ctx):
    """ Basic task information
    
        Example: invoke usage
    """
    run('invoke -l')
    print ("For information about individual task use:\n\tinvoke --help <task>\n\nExamle: invoke --help install\n")

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
        if __debug__:
            print(">>> Install OrientDB")
        run('./environment/gdb/orientdb_install.sh && cd graphdbtest && python3 insertgdb.py orientdb')
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
    directory = os.path.dirname(os.path.realpath(__file__)) + '/config/'
    configs = os.listdir(directory)
    for conf in configs:
        run('cd graphdbtest && python3 insertConf.py {}'.format(conf))
    
@task
def debug(ctx, experimentConfig=None, graphDatabaseName=None):
    """ Run experiment in debug mode
        Duplicity with invoke start, but you can see more information in terminal
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file path
        
        Example: invoke debug -d orientdb -e /path/e_select_001.conf
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "debug")
    runExperiment(ctx, graphDatabaseName, experimentConfig)
    
@task
def start(ctx, experimentConfig=None, graphDatabaseName=None):
    """ Run graph database experiment
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file path
        
        Example: invoke start -d orientdb -e /path/e_select_001.conf
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "start")
    runExperiment(ctx, graphDatabaseName, experimentConfig, False)
    
@task
def test(ctx):
    """ Caution: Run sequence of all test
        Run each defined experiment in /config directory in sequence mode for each installed database
        
        Example: invoke test
    """
    if __debug__:
        print(">>> TESTING <<<")
    directory = os.path.dirname(os.path.realpath(__file__)) + '/config/'
    configs = os.listdir(directory)
    databases = GRAPH_DATABASES
    i=0
    for conf in configs:
        conf = directory + conf
        for db in databases:
            i+=1
            if __debug__:
                print(">>>> Test no. " + str(i) + ", " + db + ", " + conf )
            start(ctx, conf, db)
            
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
    run('cd graphdbtest && python3 {opts} runtest.py -d {db} -e {ex}'.format(opts=options, db=db, ex=ex) )    

def requirements(ctx):
    """ Pip installs all requirements, and if db arg is passed, the
    requirements for that module as well 
    """
    run('python3 -m pip install -r {req}'.format(req=REQUIREMENTS))

def error(errorCode=1, errorMessage=None, task=None):
    """ End task with error
    """
    if task:
        run('invoke --help {t}'.format(t=task))
    if errorMessage:
        print ("\n [ERR] " + str(errorCode) + ": " + errorMessage)
    exit(errorCode)
