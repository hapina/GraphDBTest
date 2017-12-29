from .arangodb_conf_api import *

class ArangoDB:
    def __init__(self, dbName):
        # credentials
        self.url = GRAPHDB_API_URL 
        self.user = GRAPHDB_API_USER 
        self.password = GRAPHDB_API_PASS 
        self.dbName = dbName
        # uri for queries
        self.create = GRAPHDB_DB_CREATE
        self.importdb = GRAPHDB_DB_IMPORT
        self.batch = GRAPHDB_DB_BATCH
        self.command = GRAPH_DB_COMMAND
        self.export = GRAPHDB_DB_EXPORT
        self.drop = GRAPHDB_DB_DROP
        self.listdb = GRAPHDB_DB_LIST
        self.size = GRAPHDB_DB_SIZE
        self.defaultSchema = GRAPHDB_DB_SCHEMA
        self.dbExists = None 
 
    def setup(self):
        """
        setup 
        """
        print("WARN: ArangoDB: Not implemented yet.")
        
    def sizedb(self):
        """
        sizedb
        """  
        print("WARN: ArangoDB: Not implemented yet.")
    
    def createDB(self):
        """
        createDB 
        """  
        print("WARN: ArangoDB: Not implemented yet.")
        
    def dropDB(self):
        """
        dropDB 
        """  
        print("WARN: ArangoDB: Not implemented yet.")

    def importJSON(self, importFile):
        """
        importJSON 
        """ 
        print("WARN: ArangoDB: Not implemented yet.")
        
    def exportJSON(self, path="/tmp"):
        """
        exportJSON
        """
        print("WARN: ArangoDB: Not implemented yet.")
        
    def runCommands(self, commands):
        """
        run commands
        """
        print("WARN: ArangoDB: Not implemented yet.")
 
