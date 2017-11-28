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
        
    def importData(self, importFile):
        """
        importData - POST
        """
        req = requests.post(self.url + self.importdb + self.dbName, data=importFile, auth=(self.user , self.password))          
        if req.status_code == 200:
            print(req.json())
            result = True
        else:
            result = False
        return result
        
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

    def exportDB(self, path = "~/Downloads"):    
        """
        exportDB - GET
        """
        req = requests.get(self.url + self.export + self.dbName, auth=(self.user , self.password))  
        if req.status_code == 200:
            exportFile = path + "/exp_" + self.dbName + ".json" 
            try:
                content = gzip.decompress(req.content)
                with open(exportFile, 'wb') as f:    
                    f.write(content)            
                result = True
            except Exception as e:
                print(type(e))
                result = False
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
    my_path = "/home/hapina/Downloads/"
    db1 = "GratefulDeadConcerts"
    db2 = "testovaci_databaze"
    db3 = "GDC1000"
    gremlinCommands = []
    gremlinCommands.append('g.v("#10:1").out.map')
    gremlinCommands.append('g.V("name", "Garcia").inE("sung_by").outV.and(_().has("song_type", "original"), _().has("performances", T.gt, 1)).performances.order')
    gremlinCommands.append('g.V("name", "Garcia").inE("written_by").outV.has("song_type","original").name.order')
    dbname = db3
    
    graph = GraphDB(dbname)
    graph.setup()
    if False and graph.dbExists:
        print ("INFO: Database exists.")
        for command in gremlinCommands:
            res = graph.runCommand(command)
            #print(str(res.status_code))
            parsed_json = json.loads(res.text)
            #print(parsed_json)
        print ("INFO: Export database.")
        exportedDB = graph.exportDB(my_path)
        print('INFO: Success!' if exportedDB else 'WARN: Something is wrong here.')     
    else:
        print ("INFO: Database will be created.")
        #print(graph.createDB())
        print(graph.dbExists)
        #graph.dbName = "MyTemp4"
        #print(graph.dropDB())
        #print(graph.dbExists)
        graph.importData(my_path + "exp_GratefulDeadConcerts.json")
        print(graph.dbExists)  
        

    print ("end")

if __name__ == "__main__":
	main()

