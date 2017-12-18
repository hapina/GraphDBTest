from invoke import task, run
from datetime import date
import os
import sys

REQUIREMENTS='requirements.txt'
GRAPH_DATABASES=['orientdb', 'arangodb']

@task
def usage(ctx):
    """ Basic task information
    """
    run('invoke -l')
    print ("For information about infividual task use:\n\tinvoke --help <task>\n\tinvoke -h <task>")

@task
def clean(ctx):
    """ Clean enviroment
        - remove temporary files
    """
    print("clean")

@task
def install(ctx, database=False):
    """ Prepare enviroment for run experiments
        - isntall python3, pip and required python libraries
        - install relation database (PostgreSQL) for storing results of experiments
        - prepare database structure and run the initial load
        - prepare structure
    """
    if database:    
        if __debug__:
            print(">>> Only prepare database")
        run('cd environment && ./prepare_database.sh')
    else:
        if __debug__:
            print(">>> Install All")
        run('cd environment && ./mandatory_tools.sh && ./prepare_database.sh')
        requirements(ctx)

@task
def debug(ctx, experimentConfig=None, graphDatabaseName=None):
    """ Run experiment in debug mode
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file path
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
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "start")
    runExperiment(ctx, graphDatabaseName, experimentConfig, False)
    
@task
def test(ctx):
    """ Run all experiments defined in /config directory
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
            debug(ctx, conf, db)
            
@task
def csv(ctx, command=None, database=None, experiment=None, fileName=None, query=None):
    """ Generate experiments stats to CSV file 
        You can choose from these options:
        - command - stats relating to experiment type (select / import / create)
        - database - stats relating to particular database (orientdb / titandb / arangodb)
        - experiment - stats relating to particural experiment (ex_select_001.conf etc.)
        - query - you can create your own report with using sql query
    """
    if not fileName:
        fileName = "/tmp/report_" + str(date.today()) + ".csv"
    options=""   
    if command:
        run('cd graphdbtest && python3 {opts} gencsv.py -c {co} -f {fn}'.format(opts=options, co=command, fn=fileName) )    
    if database:
        run('cd graphdbtest && python3 {opts} gencsv.py -d {db} -f {fn}'.format(opts=options, db=database, fn=fileName) )    
    if experiment:
        run('cd graphdbtest && python3 {opts} gencsv.py -e {ex} -f {fn}'.format(opts=options, ex=experiment, fn=fileName) )   
    if query:
        run('cd graphdbtest && python3 {opts} gencsv.py -q "{qu}" -f {fn}'.format(opts=options, qu=query, fn=fileName) ) 
            
@task
def png(ctx):
    """ Generate graph in PNG file 
        - choose experiment or database 
    """
    
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
