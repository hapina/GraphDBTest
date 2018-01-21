import requests
import json

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
        self.dbExists = self.isDatabaseExist(self.dbName)
        
    def sizedb(self):
        """
        sizedb
        """  
        res = requests.get(self.url + self.size, auth=(self.user , self.password)) 
        systemInfo = json.loads(res.text)['server']
        size = json.loads(res.text)['server']['physicalMemory']
        return size

    def isDatabaseExist(self, name = None):
        """
        isDatabaseExist
        """
        if not name:
            name = self.dbName
        res = requests.get(self.url + self.listdb, auth=(self.user , self.password)) 
        listOfDB = json.loads(res.text)['result']
        return (True if listOfDB and (self.dbName in listOfDB) else False)
    
    def createDB(self):
        """
        createDB 
        """  
        data = '{{ "name": "{}" }}'.format(self.dbName)
        res = requests.post(self.url + self.create, data=data, auth=(self.user , self.password)) 
        status = (True if (res.status_code==201) else False)
        self.setup()
        if __debug__:
            if status:
                print(">>> ArangoDB create database: OK")
            else:
                print(">>> ArangoDB create database: {}".format(res.text))
        return status
        
    def dropDB(self):
        """
        dropDB 
        """  
        res = requests.delete(self.url + self.drop + self.dbName, auth=(self.user , self.password)) 
        status = (True if (res.status_code==200) else False)
        self.setup()
        if __debug__:
            if status:
                print(">>> ArangoDB create database: OK")
            else:
                print(">>> ArangoDB create database: {}".format(res.text))
        return status
            

    def importJSON(self, importFile):
        """
        importJSON 
        """ 
        data = '{{ "name": "{}" }}'.format(self.dbName)
        res = requests.post(self.url + self.importdb, data=data, auth=(self.user , self.password)) 
        status = (True if (res.status_code==201) else False)
        if __debug__:
            if status:
                print(">>> ArangoDB import database: OK")
            else:
                print(">>> ArangoDB import database: {}".format(res.text))
        return status
        
    def exportJSON(self, path="/tmp"):
        """
        exportJSON
        """
        data = '{{ "name": "{}" }}'.format(self.dbName)
        res = requests.post(self.url + self.export + "?collection=" , data=data, auth=(self.user , self.password)) 
        status = (True if (res.status_code==201) else False)
        if __debug__:
            if status:
                print(">>> ArangoDB export database: OK")
            else:
                print(">>> ArangoDB export database: {}".format(res.text))
        return status
        
    def runCommands(self, commands):
        """
        run commands
        """
        print("WARN: ArangoDB: Not implemented yet.")
 
