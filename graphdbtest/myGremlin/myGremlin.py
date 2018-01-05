import requests
import json
import re

from subprocess import Popen, PIPE

class MyGremlin:
    def __init__(self, dbName, serverName):
        # credentials
        self.url = "http://localhost:8182/"
        self.dbName = dbName
        self.serverName = serverName
        self.dbExists = None 
        
    def sizedb(self):
        """
        sizedb
        """  
        dbPath = '/tmp/{s}/{d}'.format(s=self.serverName,d=self.dbName)
        output = Popen(['du', '-s', dbPath ], stdout=PIPE).communicate()[0]
        s = output.decode("utf-8").split('\t')
        return s[0]
    
    def createDB(self):
        """
        createDB 
        """  
        database = "{}_{}".format(self.serverName,self.dbName)
        print(database)
        # upravit /opt/gremlin/conf/gremlin-server-my.yaml
        # vytvorit "/opt/gremlin/conf/{}_{}.properties".format(self.serverName,self.dbName)
        # upravit /opt/gremlin/scripts/my.groovy
        # restartovat server
        print("WARN: Gremlin: Not implemented yet.")
        return False
        
    def dropDB(self):
        """
        dropDB 
        """  
        database = "{}_{}".format(self.serverName,self.dbName)
        print(database)
        # upravit /opt/gremlin/conf/gremlin-server-my.yaml
        # smazat "/opt/gremlin/conf/{}_{}.properties".format(self.serverName,self.dbName)
        # upravit /opt/gremlin/scripts/my.groovy
        # restartovat server
        print("WARN: Gremlin: Not implemented yet.")
        return False

    def importJSON(self, importFile):
        """
        importJSON 
        """ 
        command = ["graph.io(graphson()).readGraph('{imf}')".format(imf=importFile)]
        return self.runCommands(command)
        
    def exportJSON(self, path="/tmp"):
        """
        exportJSON
        """        
        exportFile = path + "/exp_" + self.dbName + ".json"
        command = ["graph.io(graphson()).writeGraph('{exf}')".format(exf=exportFile)]
        return self.runCommands(command)
        
    def runCommands(self, commands):
        """
        run commands
        """
        objGraph = "{}_{}_graph".format(self.serverName,self.dbName)
        objG = "{}_{}_g".format(self.serverName,self.dbName)
        regexGraph = re.compile(r"^graph", re.IGNORECASE)
        regexG = re.compile(r"^g", re.IGNORECASE)
        
        for com in commands:
            com = regexGraph.sub(objGraph, com)
            com = regexG.sub(objG, com)
            data = '{{ "gremlin": "{}" , "language":"gremlin-groovy"}}'.format(com)
            if __debug__:
                print(">>>> GREMLIN-SERVER request: -X POST {url}{db} -d {data}".format(url=self.url, db=self.dbName, data=data))                   
            res = requests.post(self.url, data=data) 
            if not res or res.status_code!=200 :
                print("WARN: Gremlin-server failed for command {res}:'{com}'".format(res=res, com=com))
                if __debug__:
                    print("WARN: Gremlin-server error response: '{}'".format(res.text)) 
                return False
            else:
                if __debug__:
                    print(">>>> Gremlin-server response: {}".format(res.json()))
        if __debug__:
            print(">>>> Gremlin-server run commands: OK")
        return True

def main():
    graph = MyGremlin("testdb001", "neo4j")
    graph.createDB()
    commands = ["g.addV().property('name','first')", "graph.features()", "g.V().count()", "g.V().drop()", "g.V().count()"]
    print(graph.runCommands(commands))
    graph.exportJSON()
    graph.importJSON("/opt/gremlin/data/tinkerpop-modern.json")
    print(graph.runCommands(["g.V().outE()"]))
    print(graph.sizedb())
    graph.dropDB()
    
if __name__ == "__main__":
    main()
