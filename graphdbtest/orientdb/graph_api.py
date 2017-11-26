import pyorient 
import requests
import gzip

from graph_orientdb import *

class GraphDB:
    def __init__(self):
        self.url = GRAPHDB_API_URL 
        self.user = GRAPHDB_API_USER 
        self.password = GRAPHDB_API_PASS 
        self.dbName = "" #GRAPHDB_DBNAME 
        self.create = GRAPHDB_DB_CREATE
        self.importdb = GRAPHDB_DB_IMPORT
        self.batch = GRAPHDB_DB_BATCH
        self.export = GRAPHDB_DB_EXPORT
        self.drop = GRAPHDB_DB_DROP

    def createDB(self, schema):
        """
        createDB - POST
        """
        return requests.post(self.url + self.create + self.dbName + "/plocal", data=schema, auth=(self.user , self.password))    
    
    def importData(self, data):
        """
        importData - POST
        """
        return requests.post(self.url + self.importdb + self.dbName, data=data, auth=(self.user , self.password))          
        
    def batchCommands(self, commands):
        """
        batchCommands - GET
        """
        return requests.get(self.url + self.batch + self.dbName, data=commands, auth=(self.user , self.password))          

    def exportDB(self):    
        """
        exportDB - GET
        """
        return requests.get(self.url + self.export + self.dbName, auth=(self.user , self.password))  
    
    def dropDB(self):
        """
        dropDB - GET
        """        
        return requests.get(self.url + self.drop + self.dbName, auth=(self.user , self.password))  
    
    def size(self):
        pass

def main():
    graph = GraphDB()
    graph.dbName = "testovaci_databaze"
    #print(graph.createDB(GRAPHDB_DB_SCHEMA).json())
    e = requests.post(graph.url + GRAPHDB_DB_LIST, auth=(graph.user , graph.password))
    print(e.json())
    graph.size()
    #exportedDB = graph.exportDB()
    #print(exportedDB.status_code)
    #print(exportedDB.files)
    e = requests.post(graph.url + GRAPHDB_DB_LIST, auth=(graph.user , graph.password))
    print(e.json())
    graph.dropDB()
    e = requests.post(graph.url + GRAPHDB_DB_LIST, auth=(graph.user , graph.password))
    print(e.json())
    print ("end")

if __name__ == "__main__":
	main()

