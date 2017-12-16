import psycopg2
import sys
import time
from datetime import date

from .monitoring_conf import *
#from psycopg2 import sql

class Data:
    def __init__(self, timestamp, exper_name, gdb_name, status, repetition, run_time, size_before, size_after):
        self.timestamp = timestamp
        self.exper_name = exper_name
        self.exper_id = None
        self.gdb_name = gdb_name
        self.gdb_id = None
        self.status = status
        self.repetition = repetition
        self.run_time = run_time
        self.size_before = size_before
        self.size_after = size_after

    def getRecord(self):
        record = [self.timestamp, self.exper_id, self.gdb_id, self.status, self.repetition, self.run_time, self.size_after]
        return record

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
        self.dbConnection = None
        self.dbCursor = None

    def connection(self):
        try:
            connect_str = "dbname='" + self.dbName + "' user='" + self.user + "' host='" + self.url + "' password='" + self.password + "'"
            self.dbConnection = psycopg2.connect(connect_str)
            self.dbCursor = self.dbConnection.cursor()
            return self.dbConnection.cursor()
        except Exception as e:
            print ("Connection to the database is failed.")
            print (e)
            sys.exit(11)
    
    def execute(self, query, data = None):
        result = None
        try:
            with self.connection() as cursor:
                cursor.execute(query, data)
                if cursor.description:
                    result = cursor.fetchall()
            self.dbConnection.commit()
        finally:
            self.dbConnection.close()
        return result if result else True
    
    def insert(self, tableDefinition, data):
        query = "INSERT INTO "+ tableDefinition +" VALUES ('"
        for val in data:
            query += str(val) + "','"
        query = query[:-2] + ")"  
        if __debug__:
            print(">>> Monitoring insert: {}".format(data))
        return self.execute(query)
    
    def select(self, query):       
        return self.execute(query)

    def insertDatabase(self, data):
        """
        insertDatabase
        """
        tableDefinition = self.dbTable + " (gdb_name, gdb_description, gdb_version) "
        return self.insert(tableDefinition, data)

    def insertExperiment(self, data):
        """
        insertExperiment
        """        
        tableDefinition = self.experTable + " (exper_name, exper_description, exper_config_file) "
        return self.insert(tableDefinition, data)

    def insertRecord(self, data):
        """
        insertRecord
        """ 
        #d = Data(data)
        gdb_id = 0
        exper_config_file = data['exper_config_file']
        gdb_name = data['database']
        exper_id = self.select("select exper_id from " + self.experTable + " where exper_config_file = \'" + exper_config_file + "\'")
        gdb_id = self.select("select gdb_id from " + self.dbTable + " where gdb_name = \'" + gdb_name + "\'")
        tableDefinition = self.recTable + " (timestamp, exper_id, gdb_id, status, repetition, run_time, size_before, size_after) "
        record = [data['timestamp'], exper_id[0][0], gdb_id[0][0], data['status'], data['repetition'], data['run_time'], data['size_before'], data['size_after']] 
        return self.insert(tableDefinition, record)

    def insertValue(self, data):
        """
        insertValue
        """      
        tableDefinition = self.valueTable + " (value_name, exper_id) "
        return self.insert(tableDefinition, data)

    def exportTable(self, tableName, path = "~/Downloads", separator = ";"):    
        """
        exportTable
        """
        cur = self.connection()
        exportFile = path + "/e_" + tableName + "_" + str(date.today()) +".csv"
        #print(exportFile)
        try:
            with open(exportFile, 'w') as f:
                cur.copy_to(f, tableName, separator)
        finally:
            self.dbConnection.close()
        return True
    
    def importTable(self, importFile, tableName, separator = ";"):    
        """
        importTable
        """
        cur = self.connection()
        try:
            with open(importFile, 'r') as f:
                cur.copy_from(f, tableName, separator)
        finally:
            self.dbConnection.close()
        return True
    
    def exportDB(self, path = None):
        """
        exportDB
        """    
        pass
    
    def importDB(self, path = None):
        """
        exportDB
        """    
        pass

def main():
    print ("---")
    db = ['testovaciDB', 'Testovaci Databaze v3.3', '/opt/testdb']
    value = ['test', '7']
    exper = ('select', 'select', 'e_command_001.conf')
    record = ['2017-12-02 00:00:01', '1', '1', 'OK', 1, 2.34,0 ,0]
    mon = Monitoring()
    #mon.insertDatabase(db)
    #mon.insertExperiment(exper)
    #mon.insertRecord(record)
    #mon.insertValue(value)
    print(mon.select("SELECT * FROM GRAPH_DATABASES;"))
    print(mon.select("SELECT * FROM EXPERIMENTS_TYPES;"))
    print(mon.select("SELECT * FROM EXPERIMENTS_VALUES;"))
    print(mon.select("SELECT * FROM RECORDS;"))
    print("-")
    #mon.exportTable("graph_databases", "/home/hapina/Downloads" )
    #mon.importTable("/home/hapina/Downloads/e_graph_databases_2017-12-03.csv", "graph_databases")
    
    print(mon.select("SELECT * FROM GRAPH_DATABASES;"))
    
    print ("---")

if __name__ == "__main__":
	main()

