import sys
import time

from monitoring.monitoring import Monitoring 
    
db = sys.argv[1]
ver = sys.argv[2]
desc = sys.argv[3]
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

if not db:
    print("ERR: Choose graph database for install.")
    sys.exit(2)
    
database = {'gdb_name': db, 'gdb_description': desc, 'gdb_version': ver , 'last_update': timestamp}
mon = Monitoring()
mon.insertDatabase(database)
