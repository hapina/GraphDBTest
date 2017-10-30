import pyorient


def main():
    db_name = 'firstDB'
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("orientuser", "password")
    print (client.db_list())
    print ("connect")
    if not client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ) :
        client.db_create( db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )
    print ("db exists")
    client.db_open( db_name, "admin", "admin" )
    print (client.db_size())
    print ("db open")
    client.command("create class Animal extends V")
    client.command("insert into Animal set name = 'rat', specie = 'rodent'")
    client.query("select * from Animal")
    client.command('create class Food extends V')
    client.command("insert into Food set name = 'pea', color = 'green'")
    client.command('create class Eat extends E')
    ### Lets the rat likes to eat pea
    eat_edges = client.command(
        "create edge Eat from ("
        "select from Animal where name = 'rat'"
        ") to ("
        "select from Food where name = 'pea'"
        ")"
    )
    ### Who eats the peas?
    pea_eaters = client.command("select expand( in( Eat )) from Food where name = 'pea'")
    for animal in pea_eaters:
        print(animal.name, animal.specie)

    ### What each animal eats?
    animal_foods = client.command("select expand( out( Eat )) from Animal")
    for food in animal_foods:
        animal = client.query(
                    "select name from ( select expand( in('Eat') ) from Food where name = 'pea' )"
                )[0]
        print(food.name, food.color, animal.name)


    data = client.query('select from V', 100)
    client.db_close()

    print (data)
    print ("end")

if __name__ == "__main__":
	main()

