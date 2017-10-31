import pyorient

class graphdatabases:
    client = None
    url = "localhost"
    port = 2424
    user = "orientuser"
    password = "password"
    dbName = "firstDB"

def dbOpen():
    graphdatabases.client = pyorient.OrientDB(graphdatabases.url, graphdatabases.port)
    session_id = graphdatabases.client.connect(graphdatabases.user, graphdatabases.password)
    #print (graphdatabases.client.db_list())
    if not graphdatabases.client.db_exists( graphdatabases.dbName, pyorient.STORAGE_TYPE_MEMORY ) :
        graphdatabases.client.db_create( graphdatabases.dbName, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
    graphdatabases.client.db_open( graphdatabases.dbName, graphdatabases.user, graphdatabases.password)        
    print ("db open")

def dbClose():
    graphdatabases.client.db_close()

def dbQuery(queries):
    dbOpen()
    for query in queries:
        result = graphdatabases.client.command(query)
    dbClose()
    return result

def dbLoad():
    return graphdatabases.client

def dbCreate():
    dbOpen()
    graphdatabases.client.command("create class Animal extends V")
    graphdatabases.client.command("insert into Animal set name = 'rat', specie = 'rodent'")    
    graphdatabases.client.command('create class Food extends V')
    graphdatabases.client.command("insert into Food set name = 'pea', color = 'green'")
    graphdatabases.client.command('create class Eat extends E')
    ### Lets the rat likes to eat pea
    eat_edges = graphdatabases.client.command(
        "create edge Eat from ("
        "select from Animal where name = 'rat'"
        ") to ("
        "select from Food where name = 'pea'"
        ")"
    )
    dbClose()
    
def dbSize():
    dbOpen()
    print (graphdatabases.client.db_size())
    dbClose()

def main():
    dbSize()
    #dbCreate(client)
    print (dbQuery("select * from Animal"))
    
    ### Who eats the peas?
    pea_eaters = dbQuery("select expand( in( Eat )) from Food where name = 'pea'")
    for animal in pea_eaters:
        print(animal.name, animal.specie)
        
    ### What each animal eats?
    animal_foods = dbQuery("select expand( out( Eat )) from Animal")
    
    #for food in animal_foods:
     #   animal = graphdatabases.client.query(
      #              "select name from ( select expand( in('Eat') ) from Food where name = 'pea' )"
       #         )[0]
        #print(food.name, food.color, animal.name)


    #data = graphdatabases.client.query('select from V', 100)
    print ("end")

if __name__ == "__main__":
	main()

