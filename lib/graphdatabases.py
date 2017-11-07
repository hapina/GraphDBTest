import pyorient 

class GraphDB:
    def __init__(self, conf = dict()):
        self.client = None #conf['client']
        self.url = "localhost" #conf['url']
        self.port = 2424#conf['port']
        self.user = "orientuser" #conf['user']
        self.password = "password" #conf['password']
        self.dbName = "firstDB" #conf['dbName']

    def dbOpen(self):
        self.client = pyorient.OrientDB(self.url, self.port)
        session_id = self.client.connect(self.user, self.password)
        #print (self.client.db_list())
        if not self.client.db_exists( self.dbName, pyorient.STORAGE_TYPE_MEMORY ) :
            self.client.db_create( self.dbName, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
        self.client.db_open( self.dbName, self.user, self.password)        
        print ("db open")

    def dbClose(self):
        self.client.db_close()

    def dbQuery(self, queries):
        self.dbOpen()
        #for query in queries:
         #   result = self.client.command(query)
        result = self.client.command(queries)
        self.dbClose()
        return "OK"

    def dbLoad(self):
        return self.client

    def dbCreate(self):
        self.dbOpen()
        self.client.command("create class Animal extends V")
        self.client.command("insert into Animal set name = 'rat', specie = 'rodent'")    
        self.client.command('create class Food extends V')
        self.client.command("insert into Food set name = 'pea', color = 'green'")
        self.client.command('create class Eat extends E')
        ### Lets the rat likes to eat pea
        eat_edges = self.client.command(
            "create edge Eat from ("
            "select from Animal where name = 'rat'"
            ") to ("
            "select from Food where name = 'pea'"
            ")"
        )
        self.dbClose()
        
    def dbSize(self):
        self.dbOpen()
        size = self.client.db_size()
        print (size)
        self.dbClose()
        return size

def main():
    
    graph = GraphDB()
    graph.dbSize()
    #graph.dbCreate()
    graph.dbQuery("select * from Animal")
    print ("ok")
    print (graph.dbQuery("select * from Animal"))
    
    ### Who eats the peas?
    pea_eaters = graph.dbQuery("select expand( in( Eat )) from Food where name = 'pea'")
    for animal in pea_eaters:
        print(animal.name, animal.specie)
        
    ### What each animal eats?
    animal_foods = graph.dbQuery("select expand( out( Eat )) from Animal")
    
    #for food in animal_foods:
     #   animal = graphdatabases.client.query(
      #              "select name from ( select expand( in('Eat') ) from Food where name = 'pea' )"
       #         )[0]
        #print(food.name, food.color, animal.name)


    #data = graphdatabases.client.query('select from V', 100)
    print ("end")

if __name__ == "__main__":
	main()

