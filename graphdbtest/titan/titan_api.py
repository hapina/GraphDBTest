import requests
import json

from .titan_conf_api import *

from gremlin_python.driver import client
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection



class Titan:
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
        graph = Graph()
        g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g')) 
        g.addV('person').property('name', 'me')
        g.V()
        g.addV('person').property('name', 'you')
        t = g
        #t = g.get_graph_traversal()
        print(t)
        print(type(t))
        print(dir(t))
        v = t
        print(v)
        print("WARN: Titan: Not implemented yet.")
        
    def sizedb(self):
        """
        sizedb
        """  
        print("WARN: Titan: Not implemented yet.")
    
    def createDB(self):
        """
        createDB 
        """  
        print("WARN: Titan: Not implemented yet.")
        
    def dropDB(self):
        """
        dropDB 
        """  
        print("WARN: Titan: Not implemented yet.")

    def importJSON(self, importFile):
        """
        importJSON 
        """ 
        print("WARN: Titan: Not implemented yet.")
        
    def exportJSON(self, path="/tmp"):
        """
        exportJSON
        """
        print("WARN: Titan: Not implemented yet.")
        
    def runCommands(self, commands):
        """
        run commands
        """
        for com in commands:

            data = '{{ "gremlin": "{}" , "language":"gremlin-groovy"}}'.format(com)
            if __debug__:
                print(">>>> TITAN request: -X POST {url}{db} -d {data}".format(url=self.url, db=self.dbName, data=data))                   
            res = requests.post(self.url, data=data) 
            if not res or res.status_code!=200 :
                print("WARN: Titan failed for command {res}:'{com}'".format(res=res, com=com))
                if __debug__:
                    print("WARN: Titan error response: '{}'".format(res.text)) 
                return False
            else:
                if __debug__:
                    print(">>>> Titan response: {}".format(res.json()))
        if __debug__:
            print(">>>> Titan run commands: OK")
        return True

def main():
    titan = Titan("testdb001")
    commands = ["g.addV().property('name','first')", "graph.features()", "g.V().count()"]
    print(titan.runCommands(commands))
    #t = Titan("g")
    #t.setup()
    
if __name__ == "__main__":
    main()
