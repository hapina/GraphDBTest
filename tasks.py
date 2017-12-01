from invoke import task, run

REQUIREMENTS='requirements.txt'

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
def install(ctx):
    """ Prepare enviroment for run experiments
        - isntall python3, pip and required python libraries
        - install relation database (PostgreSQL) for storing results of experiments
        - set required enviroment variable
        - prepare structure
    """
    run('cd envinronment && ./mandatory_tools.sh')
    requirements(ctx)

@task
def debug(ctx, graphDatabaseName=None, experimentConfig=None):
    """ Run experiment in debug mode
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file path
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "debug")
    runExperiment(ctx, graphDatabaseName, experimentConfig)
    
@task
def start(ctx, graphDatabaseName=None, experimentConfig=None):
    """ Run graph database experiment
        - both arguments are mandatory 
        - graphDatabaseName: name of graph database 
        - experimentConfig: experiment configuration file path
    """
    if not graphDatabaseName or not experimentConfig:
        error(101, "Not found mandatory arguments", "start")
    runExperiment(ctx, graphDatabaseName, experimentConfig, False)
        
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
