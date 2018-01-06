import requests
import fileinput
import shutil
import json
import re
import os

from subprocess import Popen, PIPE
    
def stopGremlinServer():
    gremlinServer="/opt/gremlin/bin/gremlin-server.sh"
    output = Popen([gremlinServer, 'stop'], stdout=PIPE).communicate()[0]
    s = output.decode("utf-8").split('\t')
    return s[0]

def startGremlinServer():
    gremlinServer="/opt/gremlin/bin/gremlin-server.sh"
    output = Popen([gremlinServer, 'start'], stdout=PIPE).communicate()[0]
    s = output.decode("utf-8").split('\t')
    return s[0]

class MyGremlin:
    def __init__(self, dbName, serverName):
        # credentials
        self.url = "http://localhost:8182/"
        self.path = "/opt/gremlin/"
        self.dbName = dbName
        self.serverName = serverName
        self.dbExists = None 
        self.location = "/temp/gremlin_databases/{s}/{d}".format(s=serverName, d=dbName)
        self.confYaml = "conf/gremlin-server.yaml"
        self.confGroovy = "scripts/empty-sample.groovy"
        self.confProperties = "conf/{s}_{d}.properties".format(s=serverName, d=dbName)
        self.graphName = "{s}_{d}_graph".format(s=serverName, d=dbName)
        self.gName = "{s}_{d}_g".format(s=serverName, d=dbName)
    
    def sizedb(self):
        """
        sizedb
        """  
        output = Popen(['du', '-s', self.location ], stdout=PIPE).communicate()[0]
        s = output.decode("utf-8").split('\t')
        return s[0]
    
    def createDB(self):
        """
        createDB 
        """  
        # create location for database
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        else:
            print("[WARN] DB already exists.")
            return False
      
        stopGremlinServer()
        
        # edit /opt/gremlin/conf/gremlin-server.yaml
        yamlf= self.path + self.confYaml
        textToSearch="  graph: conf/tinkergraph-empty.properties}"
        textToReplace="  {graph}: {confP},\n{orig}".format(graph=self.graphName, confP=self.confProperties, orig=textToSearch)
        with fileinput.FileInput(files=(yamlf), inplace=True, backup='.bak') as f:
            for line in f:
                print(line.replace(textToSearch, textToReplace), end='')
                
        # edit /opt/gremlin/scripts/empty-sample.groovy
        groovyf= self.path + self.confGroovy
        with open(groovyf, "a") as f:
            f.write("\nglobals << [{g}: {graph}.traversal()]".format(g=self.gName,graph=self.graphName))
            
        # create "/opt/gremlin/conf/{}_{}.properties".format(self.serverName,self.dbName)
        propertiesf= self.path + self.confProperties
        examplePropertiesf = "{p}conf/{s}_x.properties".format(p=self.path,s=self.serverName)
        shutil.copy2(examplePropertiesf, propertiesf)
        with open(propertiesf, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()
            f.write("/{}".format(self.dbName).encode('utf-8'))
            
        startGremlinServer()
        return True

    def dropDB(self):
        """
        dropDB 
        """ 
        stopGremlinServer()
        
        # smazat /tmp/{}/{}
        if os.path.exists(self.location):
            shutil.rmtree(self.location)
        else:
            print("[WARN] DB doesn't exist.")
            return False
            
        # edit /opt/gremlin/conf/gremlin-server.yaml
        yamlf= self.path + self.confYaml
        textToSearch="  {graph}: {confP},\n".format(graph=self.graphName, confP=self.confProperties)
        textToReplace=""
        with fileinput.FileInput(files=(yamlf), inplace=True, backup='.bak') as f:
            for line in f:
                print(line.replace(textToSearch, textToReplace), end='')
                
        # edit /opt/gremlin/scripts/empty-sample.groovy
        groovyf= self.path + self.confGroovy
        textToSearch="globals << [{g}: {graph}.traversal()]".format(g=self.gName,graph=self.graphName)
        textToReplace=""
        with fileinput.FileInput(files=(groovyf), inplace=True, backup='.bak') as f:
            for line in f:
                print(line.replace(textToSearch, textToReplace), end='')
        
        # smazat "/opt/gremlin/conf/{}_{}.properties".format(self.serverName,self.dbName)
        propertiesf= self.path + self.confProperties
        if os.path.exists(propertiesf):
            os.remove(propertiesf)
            
        startGremlinServer()
        return True

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
        regexGraph = re.compile(r"^graph", re.IGNORECASE)
        regexG = re.compile(r"^g", re.IGNORECASE)
        
        for com in commands:
            com = regexGraph.sub(self.graphName, com)
            com = regexG.sub(self.gName, com)
            data = '{{ "gremlin": "{}" , "language":"gremlin-groovy"}}'.format(com)
            if __debug__:
                print(">>>> GREMLIN-SERVER request: curl -X POST -d \"{data}\" {url}{db} ".format(url=self.url, db=self.dbName, data=data))                   
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
    graph = MyGremlin("d", "neo4j")
    graph.createDB()
    print(graph.sizedb())
    commands = [ "g.addV().property('name','first')", "graph.features()", "g.V().count()", "g.V().drop()", "g.V().count()"]
    print(graph.runCommands(commands))
    graph.exportJSON()
    graph.importJSON("/opt/gremlin/data/tinkerpop-modern.json")
    print(graph.runCommands(["g.V().outE()"]))
    print(graph.sizedb())
    graph.dropDB()
    
if __name__ == "__main__":
    main()
