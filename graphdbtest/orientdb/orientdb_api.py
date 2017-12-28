import requests
import json
import gzip

from .orientdb_conf_api import *

class GraphDB:
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
        self.defaultSchema = GRAPHDB_DB_SCHEMA_0
        self.dbExists = None
        
    def setup(self):
        """
        setup - setup dbName 
        """
        self.dbExists = self.isDatabaseExist(self.dbName)

    def createDB(self, schema = None):
        """
        createDB - POST
        """
        if not schema:
            schema = self.defaultSchema
        res = requests.post(self.url + self.create + self.dbName + "/plocal", data=schema, auth=(self.user , self.password))    
        self.dbExists = (True if (res.status_code==200) else False)
        if __debug__:
            print(">>> ORIENTDB create database: OK")
        return self.dbExists
        
    def importData(self, importFile):
        """
        importData - POST
        """
        res = requests.post(self.url + self.importdb + self.dbName  + "?merge=true", data=importFile, auth=(self.user , self.password))       
        if res and res.status_code == 200:
            print(res.json())
            #parsed_json = json.loads(res.text)
            #print(parsed_json)
            result = True
        else:
            result = False
        return result
        
    def runBatch(self, batch):
        """
        run batch - POST
        """
        return requests.get(self.url + self.batch + self.dbName, data=batch, auth=(self.user , self.password))          

    def runCommands(self, commands):
        """
        run commands - POST
        """
        for com in commands:
            if __debug__:
                print(">>>> ORIENTDB command: -u {u}:{p} {url}{com}{db}/gremlin {data}".format(u=self.user, p=self.password, url=self.url, com=self.command, db=self.dbName, data=com))            
            res = requests.post(self.url + self.command + self.dbName + "/gremlin/", data=com, auth=(self.user , self.password)) 
            if not res or res.status_code!=200 :
                print("WARN: OrientDB failed for command {res}:'{com}'".format(res=res, com=com))
                if __debug__:
                    print("WARN: OrientDB error response: '{}'".format(res.json())) 
                return False
        if __debug__:
            print(">>>> ORIENTDB run commands: OK")
        return True

    def exportToJSON(self, path = "/tmp"):
        """
        exportToCSV - POST
        """
        headers = {'Accept': 'text/json'}
        commands = ("g.V", "g.E")
        for com in commands:
        #com = "g.V"
            res = requests.post(self.url + self.command + self.dbName + "/gremlin/", data=com, auth=(self.user , self.password), headers=headers) 
            items = str(json.loads(res.text)['result'])
           # print(items)
            if not res or res.status_code!=200 :
                print("WARN: " + com)
                return False
            exportFile = path + "/exp_" + self.dbName + "_" + com + ".json" 
            with open(exportFile, 'w') as f:    
                f.write(items)   
            print("JSON Export: " + exportFile)
        return True
    
    def exportDB(self, path = "/tmp"):    
        """
        exportDB - GET
        """
        res = requests.get(self.url + self.export + self.dbName, auth=(self.user , self.password))  
        if res and res.status_code == 200:
            exportFile = path + "/exp_" + self.dbName + ".json" 
            try:
                content = gzip.decompress(res.content)
                with open(exportFile, 'wb') as f:    
                    f.write(content)            
                result = True
            except Exception as e:
                print(type(e))
                result = False
        else: 
            if res:
                print(str(res.status_code) + ": " + res.json())
            result = False
        return result
        
    def dropDB(self):
        """
        dropDB - DELETE
        """      
        if self.dbExists:
            res = requests.delete(self.url + self.drop + self.dbName, auth=(self.user , self.password)) 
            if res and res.status_code == 204:
                self.dbExists = False
                return True
            else:
                if res:
                    print(str(res.status_code) + res.json())
                return False
        else:
            print("WARN: database is not exist.")
            return False
    
    def isDatabaseExist(self, name = None):
        """
        isDatabaseExist - GET
        """
        if not name:
            name = self.dbName
        res = requests.get(self.url + self.listdb, auth=(self.user , self.password)) 
        listOfDB = json.loads(res.text)['databases']
        return (True if listOfDB and (self.dbName in listOfDB) else False)
    
    def sizedb(self):
        """
        size of database - GET   
        ORIENTDB ERROR:       
        "content": "java.lang.IllegalArgumentException: 
            Cannot get allocation information for database 'GratefulDeadConcerts' 
            because it is not implemented yet."
        """
        requests.get(self.url + self.size + self.dbName, auth=(self.user , self.password)) 
        return 1452

def main():
    test = False
    my_path = "/home/hapina/Downloads/"
    db1 = "GratefulDeadConcerts"
    db2 = "testovaci_databaze"
    db3 = "test"
    db4 = "test0002"
    
    gremlinCommands = []
    gremlinCommands.append('g.v("#10:1").out.map')
    gremlinCommands.append('g.V("name", "Garcia").inE("sung_by").outV.and(_().has("song_type", "original"), _().has("performances", T.gt, 1)).performances.order')
    gremlinCommands.append('g.V("name", "Garcia").inE("written_by").outV.has("song_type","original").name.order')
    dbname = db3
    
    print ("---")    
    #graph = GraphDB(dbname)
    #graph.setup()
    #graph.exportDB(my_path)
    
    graph2 = GraphDB(db4)
    graph2.setup()
    graph2.dropDB()
    graph2.createDB()
    graph2.importData(my_path + "exp_test.json")
    
    if test:
        e = graph.dbExists
        if not e:
            print ("INFO: CreateDB")
            if not graph.createDB():
                print("WARN: Failed createDB for " + dbname)         
            print ("INFO: ImportData")     
            if not graph.importData(my_path + "exp_GratefulDeadConcerts.json"):
                print("WARN: Failed importData for " + dbname)
                
        print ("INFO: Run Commnads")
        if not graph.runCommand(gremlinCommands):
            print("WARN: Failed runCommand for " + dbname)
        print ("INFO: Export database.")
        if not graph.exportDB(my_path):
            print("WARN: Failed exportDB for " + dbname)     
        if not e:                        
            print ("INFO: DropDB and check of exists")   
            if not graph.dropDB() or graph.dbExists:
                print("WARN: Failed dropDB for " + dbname)
            print ("INFO: Check of existance")   
    print ("---")

if __name__ == "__main__":
	main()

