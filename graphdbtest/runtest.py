import time
import sys
import getopt

from orientdb.orientdb_api import GraphDB
from setupConf import Configuration
from monitoring.monitoring import Monitoring

def select(gdb, rec):
    for i in range(int(rec['repetition'])):
        start_time = time.time()
        if __debug__:
            print(">>> " + str(i) + ". SELECT")
        if not gdb.runCommand(rec['commands']):
            print("WARN: Failed runCommand for " + rec['gdb_name'] )
        else:
            rec['status'] = "OK"
        rec['run_time'] = (time.time()-start_time)
        rec['size_before'] = 0.0
        rec['size_after'] = 0.0 
        mon = Monitoring()
        mon.insertRecord(rec)


def main():
    #------------------------------ Zpracovani vstupnich argumentu      
    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:d:", ["experiment=", "database="])
    except getopt.GetoptError as err:
        print (err)
        usage()
        sys.exit(2)
        
    experiment = database = None
    
    for o, a in opts:
        if o in ("-e", "--experiment"):
            experiment = a
        elif o in ("-d", "--database"):
            database = a
        else:
            assert False, "unhandled option."
    
    #------------------------------ Configuration
    exper = Configuration(experiment)
    exper.setupConf() 
    #monitoring = True if exper.get('monitoring')=='yes' else False
    record = dict()
    record['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    record['exper_config_file'] = experiment[(experiment.rfind('/') + 1):]
    record['gdb_name'] = exper.get('db_name')
    record['database'] = database
    record['repetition'] = exper.get('repetition')
    record['experiment_type'] = exper.get('experiment_type')
    record['status'] = 'ERR'
    
    #------------------------------ Graph database
    if database=="orientdb":
        g = GraphDB(record['gdb_name'])
        g.setup()
    else:
        print("WARN: Not implemented yet.")
        return 3
    
    #------------------------------ Run Experiment
    if record['experiment_type'] == 'select':
        record['commands'] = exper.get('commands').split("|")
        select(g, record)
    else:
        print("WARN: Not implemented yet.")  
        return 3

if __name__ == "__main__":
    main()
