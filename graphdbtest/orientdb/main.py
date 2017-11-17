import pyorient 
from .local import *

class GraphDB:
    def __init__(self):
        self.client = ORIENTDB_CLIENT
        self.url = ORIENTDB_URL 
        self.port = ORIENTDB_PORT 
        self.user = ORIENTDB_USER 
        self.password = ORIENTDB_PASS 
        self.dbName = ORIENTDB_DBNAME 

    def connect(self):
        self.client = pyorient.OrientDB(self.url, self.port)
        session_id = self.client.connect(self.user, self.password)
       # print (self.client.db_list())
        if not self.client.db_exists( self.dbName, pyorient.STORAGE_TYPE_MEMORY ) :
            self.client.db_create( self.dbName, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
        self.client.db_open( self.dbName, self.user, self.password)        
        print ("connect")

    def disconnect(self):
        print("disconnect")
        self.client.db_close()

    def read(self, queries):
        self.connect()
        result = ""
        #sprint( len(queries))
        #if len(queries) > 1:
         #   for query in queries:
          #      result += self.client.command(query)
        result = self.client.command(queries)
        self.disconnect()
        return result

    def load(self):
        return self.client

    def insert(self):
        self.connect()
        self.client.command("create class Animal extends V")
        self.client.command("insert into Animal set name = 'rat', specie = 'rodent'")    
        self.client.command('create class Food extends V')
        self.client.command("insert into Food set name = 'pea', color = 'green'")
        self.client.command('create class Eat extends E')
        ### Lets the rat likes to eat pea
        #eat_edges = self.client.command(
         #   "create edge Eat from ("
         #   "select from Animal where name = 'rat'"
         #   ") to ("
         #   "select from Food where name = 'pea'"
         #   ")"
        #)
        self.disconnect()
        
    def size(self):
        self.connect()
        size = self.client.db_size()
        print (size)
        self.disconnect()
        return size

def main():
    
    graph = GraphDB()
    graph.size()
    graph.insert()
    print("first select")
    graph.read("select * from V")
    print ("ok")
    #graph.read("select * from Animal")
   # print("second select OK")
   # print (graph.read("select * from Animal"))
    
    ### Who eats the peas?
    #pea_eaters = graph.read("select expand( in( Eat )) from Food where name = 'pea'")
    #for animal in pea_eaters:
    #    print(animal.name, animal.specie)
        
    ### What each animal eats?
   # animal_foods = graph.read("select expand( out( Eat )) from Animal")
    
    #for food in animal_foods:
     #   animal = graphdatabases.client.query(
      #              "select name from ( select expand( in('Eat') ) from Food where name = 'pea' )"
       #         )[0]
        #print(food.name, food.color, animal.name)


    #data = graphdatabases.client.query('select from V', 100)
    print ("end")

if __name__ == "__main__":
	main()

