import requests
import json
import gzip

from graph_orientdb import *

class GraphDB:
    def __init__(self, dbName = None):
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
        self.defaultSchema = GRAPHDB_DB_SCHEMA_0
        self.dbExists = None
        
    def setup(self, dbName = None):
        """
        setup - setup dbName 
        """
        self.dbExists = self.isDatabaseExist(dbName)

    def createDB(self, schema = None):
        """
        createDB - POST
        """
        if not schema:
            schema = self.defaultSchema
        req = requests.post(self.url + self.create + self.dbName + "/plocal", data=schema, auth=(self.user , self.password))    
        self.dbExists = (True if (req.status_code==200) else False)
        return self.dbExists
        
    def importData(self, data):
        """
        importData - POST
        """
        return requests.post(self.url + self.importdb + self.dbName, data=data, auth=(self.user , self.password))          
        
    def runBatch(self, batch):
        """
        run batch - POST
        """
        return requests.get(self.url + self.batch + self.dbName, data=batch, auth=(self.user , self.password))          

    def runCommand(self, commands):
        """
        run commands - POST
        """
        return requests.post(self.url + self.command + self.dbName + "/gremlin/", data=commands, auth=(self.user , self.password))          

    def exportDB(self):    
        """
        exportDB - GET
        """
        req = requests.get(self.url + self.export + self.dbName, auth=(self.user , self.password))  
        if req.status_code == 200:
            print(req.raw)    
            result = True
        else: 
            print("Error in exportDB: " + str(req.status_code) + req.json())
            result = False
        return result
        
    def dropDB(self):
        """
        dropDB - DELETE
        """        
        if self.dbExists:
            req = requests.delete(self.url + self.drop + self.dbName, auth=(self.user , self.password)) 
            if req.status_code == 204:
                self.dbExists = False
                return True
            else:
                print(req.json())
                return False
        else:
            error("ERROR: database is not exist.")
            return False
    
    def isDatabaseExist(self, name = None):
        """
        isDatabaseExist - GET
        """
        if not name:
            name = self.dbName
        req = requests.get(self.url + self.listdb, auth=(self.user , self.password)) 
        listOfDB = json.loads(req.text)['databases']
        return (True if listOfDB and (self.dbName in listOfDB) else False)
    
    def sizedb(self):
        """
        size of database - GET   
        ORIENTDB ERROR:       
        "content": "java.lang.IllegalArgumentException: 
            Cannot get allocation information for database 'GratefulDeadConcerts' 
            because it is not implemented yet."
        """
        return requests.get(self.url + self.size + self.dbName, auth=(self.user , self.password)) 

def main():
    db1 = "GratefulDeadConcerts"
    db2 = "testovaci_databaze"
    db3 = "myTemp7"
    gremlinCommands = []
    gremlinCommands.append('g.v("#10:1").out.map')
    gremlinCommands.append('g.V("name", "Garcia").inE("sung_by").outV.and(_().has("song_type", "original"), _().has("performances", T.gt, 1)).performances.order')
    gremlinCommands.append('g.V("name", "Garcia").inE("written_by").outV.has("song_type","original").name.order')
    dbname = db1
    
    graph = GraphDB(dbname)
    graph.setup()
    if graph.dbExists:
        print ("INFO: Database exists.")
        for command in gremlinCommands:
            res = graph.runCommand(command)
            #print(str(res.status_code))
            parsed_json = json.loads(res.text)
            #print(parsed_json)
        exportedDB = graph.exportDB()
        print(exportedDB)     
    else:
        print ("INFO: Database will be created.")
        print(graph.createDB())
        print(graph.dbExists)
        graph.dbName = "MyTemp4"
        #print(graph.dropDB())
        print(graph.dbExists)
        #graph.importDB()

    print ("end")

if __name__ == "__main__":
	main()

