""" ORIENT DB
"""

# access from python
GRAPHDB_CLIENT = None
GRAPHDB_URL = "localhost"
GRAPHDB_PORT = 2424
GRAPHDB_USER = "orientuser"
GRAPHDB_PASS = "password"
GRAPHDB_DBNAME = "firstDB"

# access from HTTP API
GRAPHDB_API_URL = "http://localhost:2480"
GRAPHDB_API_USER = "orientuser"
GRAPHDB_API_PASS = "password"
GRAPHDB_API_DBNAME = ""
GRAPHDB_DB_LIST = "/listDatabases"  # GET
GRAPHDB_DB_CREATE = "/database/"    # POST
GRAPHDB_DB_DROP = "/database/"      # DELETE
GRAPHDB_DB_EXPORT = "/export/"      # GET
GRAPHDB_DB_BATCH = "/batch/"     # POST
GRAPH_DB_COMMAND = "/command/"   #POST
GRAPHDB_DB_IMPORT = "/import/"   # POST
GRAPHDB_DB_SIZE = "/allocation/" #GET
GRAPHDB_DB_SCHEMA_0 = ''
GRAPHDB_DB_SCHEMA_1 = '{"classes":[]}' 
GRAPHDB_DB_SCHEMA_2 = '{"classes":[{"id":0,"name":"ORole","clusters":[3],"defaultCluster":3,"records":0},{"id":1,"name":"OUser","clusters":[4],"defaultCluster":4,"records":0}]}'
