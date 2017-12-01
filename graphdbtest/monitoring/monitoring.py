import psycopg2
import sys

from monitoring_conf import *
from psycopg2 import sql

class Monitoring:
    def __init__(self):
        self.url = MONITORING_URL 
        self.user = MONITORING_USER 
        self.password = MONITORING_PASS 
        self.dbName = MONITORING_DBNAME
        self.dbTable = MONITORING_DB_TABLE
        self.recTable = MONITORING_REC_TABLE
        self.experTable = MONITORING_EXPER_TABLE
        self.valueTable = MONITORING_VALUE_TABLE

    def connection(self):
        try:
            connect_str = "dbname='" + self.dbName + "' user='" + self.user + "' host='" + self.url + "' password='" + self.password + "'"
            conn = psycopg2.connect(connect_str)
            return conn.cursor()
        except Exception as e:
            print ("Connection to the database is failed.")
            print (e)
            sys.exit(11)
            
    def execute(self, query, data = None):
        connection = self.connection()
        connection.execute(query, data)
        result = connection.fetchall()
        if not result:
            result = "nic"
        #connection.close()
        return result
    
    def insert(self, table, data):
        query = sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)").format(sql.Identifier(table))        
        return self.execute(query, data)
    
    def select(self, query):       
        return self.execute(query)

    def insertDatabase(self, data):
        """
        insertDatabase
        """
        return self.insert(self.dbTable, data)

    def insertExperiment(self, data):
        """
        insertExperiment
        """
        return self.insert(self.experTable, data)

    def insertRecord(self, data):
        """
        insertRecord
        """
        return self.insert(self.recTable, data)


    def insertValue(self, data):
        """
        insertRecord
        """
        return self.insert(self.valueTable, data)

    def exportDB(self, path = "~/Downloads"):    
        """
        exportDB
        """
        pass
    
    def importDB(self, importFile):    
        """
        importDB
        """
        pass

def main():
    print ("---")
    db = ['orientdb', 'orientdb', 'OrientDB v2.2 document-graph database', '/opt/orientdb']
    value = ['001', 'orientdb', 'OrientDB v2.2 document-graph database', '/opt/orientdb']
    exper = ('001', 'select', 'select', 'e_command_001.conf')
    record = ['0001', '', '001', '001', 'OK', 1, 234, None, None]
    mon = Monitoring()
    mon.connection()
    mon.insertDatabase(db)
   # mon.insertExperiment(exper)
   # mon.insertRecord(record)
   # mon.insertValue(value)
    print(mon.select("SELECT * FROM GRAPH_DATABASES;"))
    print ("---")

if __name__ == "__main__":
	main()

