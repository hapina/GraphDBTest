import psycopg2
import sys

from monitoring_conf import *

class Monitoring:
    def __init__(self):
        self.url = MONITORING_URL 
        self.user = MONITORING_USER 
        self.password = MONITORING_PASS 
        self.dbName = MONITORING_DBNAME
        self.dbTable = MONITORING_DB_TABLE
        self.recTable = MONITORING_REC_TABLE
        self.experTable = MONITORING_EXPER_TABLE

    def connection(self):
        try:
            connect_str = "dbname='" + self.dbName + "' user='" + self.user + "' host='" + self.url + "' password='" + self.password + "'"
            conn = psycopg2.connect(connect_str)
            return conn.cursor()
        except Exception as e:
            print ("Connection to the database is failed.")
            print (e)
            sys.exit(11)
            
    def execute(self, query, data):
        connection = self.connection()
        connection.execute(query, data)
        result = connection.fetchall()
        #connection.close()
        return result
    
    def insert(self, table, data):
        query = sql.SQL("INSERT INTO {} VALUES (%s, %s)").format(sql.Identifier(table))        
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
        pass
    print ("---")
    mon = Monitoring()
    mon.connection()
    mon.insertDatabase()
    mon.insertExperiment()
    mon.insertRecord()
    mon.select("SELECT * FROM RECORD;")
    print ("---")

if __name__ == "__main__":
	main()

