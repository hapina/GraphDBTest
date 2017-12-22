import psycopg2
import sys
import time
from datetime import date

from .monitoring_conf import *

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
        self.dbConnection = None
        self.dbCursor = None
        
        self.gdbTab = MONITORING_GDB_TABLE
        self.measTab = MONITORING_MEAS_TABLE 
        self.confTab = MONITORING_CONF_TABLE
        self.typeTab = MONITORING_TYPE_TABLE
        self.expTab = MONITORING_EXP_TABLE
        self.iteTab = MONITORING_ITE_TABLE
        self.valTab = MONITORING_VAL_TABLE

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
    
    def getId(self, table, name, colId, colName):
        id = self.execute("SELECT {cId} FROM {tab} WHERE {cN}='{n}';".format(tab=table, n=name, cId=colId, cN=colName))
        return id[0][0]
    
    def insertDatabase(self, data):
        """
        insertDatabase
        """
        insert = [data['gdb_name'], data['gdb_description'], data['gdb_version']]
        tableDefinition = self.gdbTab + " (gdb_name, gdb_description, gdb_version) "
        return self.insert(tableDefinition, insert)

    def insertExperiment(self, data):
        """
        insertExperiment    
        """
        if not 'gdb_id' in data:
            if 'gdb_name' in data:
                data['gdb_id'] = self.getId(self.gdbTab, data['gdb_name'], 'gdb_id', 'gdb_name') 
            else:
                print("ERR: Cannot insert data, missing parameter gdb_id")
                sys.exit(12)
        if not 'conf_id' in data:
            if 'conf_name' in data:
                data['conf_id'] = self.getId(self.confTab, data['conf_name'], 'conf_id', 'conf_name') 
            else:
                print("ERR: Cannot insert data, missing parameter conf_id")
                sys.exit(12)
        insertData = [data['run_date'], data['iteration_count'], data['gdb_id'], data['conf_id']]
        if __debug__:
            print("INFO: insert Experiment ({})".format(insertData))
        tableDefinition = self.expTab + " (run_date, iteration_count, gdb_id, conf_id) "
        return self.insert(tableDefinition, insertData)

    def insertIteration(self, data):
        """
        insertRecord
        """       
        insertData=[data['iter_timestamp'], data['iter_number'], data['status'], data['exper_id']]
        if __debug__:
            print("INFO: insert Iteration ({})".format(insertData))
        tableDefinition = self.iteTab + " (iter_timestamp, iter_number, status, exper_id) "
        return self.insert(tableDefinition, insertData)

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
    
    def getReportQuery(self, command=None, database=None, experiment=None):
        query = "SELECT * FROM records WHERE status='OK'"
        if experiment:
            query += " AND exper_id='{}'".format(experiment)
        if database:
            query += " AND gdb_id='{}'".format(database)
        if command:
            query += " AND type_id='{}'".format(command)
        query += " ORDER BY timestamp"
        return query
    
    def copyToCSV(self, query, csvFile):
        copyQuery = "COPY ({}) TO STDOUT WITH CSV".format(query)
        try:
            with self.connection() as cursor:
                with open(csvFile, 'w') as f:
                    cursor.copy_expert(copyQuery, f)
                print("INFO: CSV file was created - {}".format(csvFile))
        finally:
            self.dbConnection.close()

def main():
    print ("---")
    db = {'gdb_name': 'testovaciDB', 'gdb_description': 'Testovaci Databaze', 'gdb_version': '2.5.4'}
    exper = {'run_date': '2017-12-13 00:00:01', 'iteration_count': 3}
    #exper['gdb_id']=1
    exper['gdb_name']='testovaciDB'
    #exper['conf_id']=1
    exper['conf_name']='e_select_001.conf'
    #value = ['test', '7']
    iteration = {'iter_timestamp': '2017-12-02 00:00:01', 'iter_number': 1, 'status': 'OK', 'exper_id':1}
    mon = Monitoring()
    #mon.insertDatabase(db)
    #mon.insertExperiment(exper)
    mon.insertIteration(iteration)
    #mon.insertValue(value)
    print(mon.select("SELECT * FROM ITERATION;"))
    #print(mon.select("SELECT * FROM EXPERIMENT;"))
    print("-")
    #mon.exportTable("graph_databases", "/home/hapina/Downloads" )
    #mon.importTable("/home/hapina/Downloads/e_graph_databases_2017-12-03.csv", "graph_databases")
    
    print ("---")

if __name__ == "__main__":
	main()

