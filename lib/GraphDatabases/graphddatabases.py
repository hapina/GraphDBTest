import pyorient


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("admin", "admin_passwd")

data = client.query("SELECT FROM Sensors "
                    "WHERE sensorType = 'Pollen'", 
                    100)
