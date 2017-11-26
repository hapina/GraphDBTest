import pyorient 
import requests

from graph_orientdb import *
from gremlin_python.driver import client 

class GraphDB:
    def __init__(self):
        self.client = GRAPHDB_CLIENT
        self.url = GRAPHDB_URL 
        self.port = GRAPHDB_PORT 
        self.user = GRAPHDB_USER 
        self.password = GRAPHDB_PASS 
        self.dbName = GRAPHDB_DBNAME 

    def connect(self):
        pass

    def disconnect(self):
        pass
   
    def read(self, queries):
        pass

    def load(self):
        pass

    def insert(self):
        pass
        
    def size(self):
        pass

def main():
    c = client.Client('ws://localhost:8182/graph', 'g')
    #print(c.g.V())
    c.close()  
    print("the end")

if __name__ == "__main__":
	main()

 
