""" GRAPH DB
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
GRAPHDB_API_USER = "root"
GRAPHDB_API_PASS = "root"
GRAPHDB_DB_LIST = "/listDatabases"  # GET
GRAPHDB_DB_CREATE = "/database/"    # POST
GRAPHDB_DB_DROP = "/database/"      # DELETE
GRAPHDB_DB_EXPORT = "/export/"      # GET
GRAPHDB_DB_BATCH = "/batch/"     # POST
GRAPHDB_DB_IMPORT = "/import/"   # POST

GRAPHDB_DB_SCHEMA = '{"classes":[{"id":0,"name":"ORole","clusters":[3],"defaultCluster":3,"records":0},{"id":1,"name":"OUser","clusters":[4],"defaultCluster":4,"records":0}]}'
