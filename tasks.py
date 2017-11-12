from invoke import task, run

REQUIREMENTS='requirements.txt'

@task
def help(ctx):
    """ Basic task information
    """
    run('invoke -l')

@task
def uninstall(ctx):
    """ Clean enviroment
    """
    print("clean")

@task
def install(ctx):
    """ Prepare enviroment for run experiments
    """
    requirements(ctx)
    print("install")
    
@task
def runtest(ctx, db=None, ex=None):
    """ Starts the experiment for the set database 
    """
    if not db or not ex:
        print("ERROR Not found mandatory arguments \n Usage: invoke runtest --db db.cfg --ex ex.cfg")
        exit(1001)
    run('cd graphdbtest && python3 runtest.py {db} {ex}'.format(db=db, ex=ex) )
        
def requirements(ctx):
    """ Pip installs all requirements, and if db arg is passed, the
    requirements for that module as well """

    run('python3 -m pip install -r {req}'.format(req=REQUIREMENTS))
