import time
import sys
import getopt

from orientdb.orientdb_api import GraphDB
from setupConf import Configuration
from monitoring.monitoring import Monitoring

def select(gdb, rec, mon):
    if __debug__:
        print("----------")
    for i in range(int(rec['iteration_count'])):
        start_time = time.time()
        if __debug__:
            print(">>> " + str(i+1) + ". SELECT")
        if not gdb.runCommands(rec['commands']):
            print("WARN: Failed runCommand for " + rec['gdb_name'] )
        else:
            rec['status'] = "OK"
        rec['iter_timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        rec['iter_number'] = i+1
        rec['value']['run_time'] = (time.time()-start_time)
        rec['iter_id'] = mon.insertIteration(rec)
        mon.insertValues(rec)
        if __debug__:
            print(">>>> experiment: {}".format(rec))
    if __debug__:
        print("----------")


def main():
    #------------------------------ Zpracovani vstupnich argumentu      
    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:d:", ["experiment=", "database="])
    except getopt.GetoptError as err:
        print (err)
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
    record['run_date'] = time.strftime("%Y-%m-%d %H:%M:%S")
    record['conf_name'] = experiment[(experiment.rfind('/') + 1):]
    record['database'] = exper.get('db_name')
    record['gdb_name'] = database
    record['type_name'] = exper.get('experiment_type')
    record['status'] = 'ERR'
    record['value'] = dict()
    
    #------------------------------ Graph database
    if database=="orientdb":
        g = GraphDB(record['database'])
        g.setup()
    else:
        print("WARN: Not implemented yet.")
        return 3
    
    #------------------------------ Run Experiment
    if record['type_name'] in ['create','drop']:
        start_time = time.time()
        if record['type_name'] == 'create':
            res = g.createDB()
        if record['type_name'] == 'drop':
            res = g.dropDB()
        if res:
            record['status'] = "OK"
            record['value']['run_time'] = (time.time()-start_time)
            record['value']['size'] = g.sizedb() 
        mon = Monitoring()
        record['iteration_count'] = 1
        record['exper_id'] = mon.insertExperiment(record)
        record['iter_timestamp'] = record['run_date']
        record['iter_number'] = 1
        record['iter_id'] = mon.insertIteration(record)
        mon.insertValues(record)
        if __debug__:
            print(">>>> experiment: {}".format(record))
        
    elif record['type_name'] in ['insert','delete']:
        record['iteration_count'] = 1
        record['commands'] = exper.get('commands').split("\n|")
        mon = Monitoring()
        record['exper_id'] = mon.insertExperiment(record)
        record['value']['size'] = g.sizedb() 
        start_time = time.time()
        if g.runCommands(record['commands']):
            record['status'] = "OK"
            record['value']['size_after'] = g.sizedb() 
        record['iter_timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        record['iter_number'] = 1
        record['value']['run_time'] = (time.time()-start_time)
        record['iter_id'] = mon.insertIteration(record)
        mon.insertValues(record)
        if __debug__:
            print(">>>> experiment: {}".format(record))
        
    elif record['type_name'] == 'select':
        record['iteration_count'] = exper.get('iteration')
        record['commands'] = exper.get('commands').split("|")
        mon = Monitoring()
        record['exper_id'] = mon.insertExperiment(record)
        record['value']['size'] = g.sizedb() 
        select(g, record, mon)
        
    elif record['type_name'] == 'import':
        print("WARN: Not implemented yet.") 
        
    elif record['type_name'] == 'export':
        start_time = time.time()
        if g.exportDB():
            record['status'] = "OK"
            record['value']['run_time'] = (time.time()-start_time)
            record['value']['size'] = g.sizedb() 
        mon = Monitoring()
        record['iteration_count'] = 1
        record['exper_id'] = mon.insertExperiment(record)
        record['iter_timestamp'] = record['run_date']
        record['iter_number'] = 1
        record['iter_id'] = mon.insertIteration(record)
        mon.insertValues(record)
        if __debug__:
            print(">>>> experiment: {}".format(record))
        
    else:
        print("WARN: Not implemented yet.")  
        return 3

if __name__ == "__main__":
    main()
