import sys
import time

from monitoring.monitoring import Monitoring 
    
db = sys.argv[1]
ver = sys.argv[2]
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
if not db:
    print("ERR: Choose graph database for install.")
    sys.exit(2)
    
if db == 'orientdb':
    database = {'gdb_name': 'orientdb', 'gdb_description': 'OrientDB, document-graph database', 'gdb_version': ver , 'last_update': timestamp}
elif db == 'janusgraph':
    database = {'gdb_name': 'janusgraph', 'gdb_description': 'JanusGraph & Cassandra, distributed graph database', 'gdb_version': ver , 'last_update': timestamp}   
elif db == 'arangodb':
    database = {'gdb_name': 'arangodb', 'gdb_description': 'Arango DB, native multi-model database', 'gdb_version': ver , 'last_update': timestamp}    
#"titanC","Titan & Cassandra, distributed graph database ","v1.0"
#"titanH","Titan & HBase, distributed graph database","v1.0"
#"titanB","Titan & BerkeleyDB, distributed graph database","v1.0"
#"titanM","Titan & InMemory, distributed graph database","v1.0"
else:
    print("WARN: Not implemented yet for database - {}".format(db))
    sys.exit(12)
    
mon = Monitoring()
mon.insertDatabase(database)
