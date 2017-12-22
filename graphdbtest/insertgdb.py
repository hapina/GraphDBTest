import sys

from monitoring.monitoring import Monitoring 
    
db = sys.argv[1]
if not db:
    print("ERR: Choose graph database for install.")
    sys.exit(2)
    
if db == 'orientdb':
    database = {'gdb_name': 'orientdb', 'gdb_description': 'OrientDB, document-graph database', 'gdb_version': 'v2.0'}
#"titanC","Titan & Cassandra, distributed graph database ","v1.0"
#"titanH","Titan & HBase, distributed graph database","v1.0"
#"titanB","Titan & BerkeleyDB, distributed graph database","v1.0"
#"titanM","Titan & InMemory, distributed graph database","v1.0"
#"arangodb","Arango DB, native multi-model database","v3.2"    
else:
    print("WARN: Not implemented yet for database - {}".format(db))
    sys.exit(12)
    
mon = Monitoring()
mon.insertDatabase(database)
