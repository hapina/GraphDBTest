import psycopg2
import sys
import time
from datetime import date

from .monitoring_conf import *

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
    
    def insert(self, tableName, data, update=None):
        columnName = insertData = insertCondition = ""
        if update:
            updateData = ""
            for key, val in data.items():
                updateData += "{key}='{val}', ".format(val=val, key=key)
            updateQuery = "UPDATE {tab} SET {data} WHERE {cond}".format(tab=tableName, data=updateData[:-2], cond=update)
            insertCondition = "WHERE NOT EXISTS (SELECT 1 FROM {tab} WHERE {cond})".format(tab=tableName, cond=update)
            if __debug__:
                print(">>>> MONITORING Insert SQL: {}".format(updateQuery))
            self.execute(updateQuery)
        for key, val in data.items():
            columnName += "{}, ".format(key)  
            insertData += "'{}',".format(val)  
        insertQuery = "INSERT INTO {tab} ({cn}) SELECT {id} {cond}".format(tab=tableName, cn=columnName[:-2], id=insertData[:-1], cond=insertCondition)
        if __debug__:
            print(">>>> MONITORING Insert SQL: {}".format(insertQuery))
        return self.execute(insertQuery)

    def select(self, query):       
        return self.execute(query)
    
    def getId(self, table, name, colId, colName, extension=''):
        id = self.execute("SELECT {cId} FROM {tab} WHERE {cN}='{n}' {ex};".format(tab=table, n=name, cId=colId, cN=colName, ex=extension))
        if type(id)==bool:
            return 0
        else:
            return id[0][0]
    
    def insertDatabase(self, data):
        """
        insertDatabase
        """
        #insertOrUpdate = "gdb_server='{db}' and gdb_version='{ver}'".format(db=data['gdb_server'], ver=data['gdb_version'])
        return self.insert(self.gdbTab, data)
    
    def insertConfiguration(self, conf_name):
        """
        insertConfiguration
        """
        insert = {'conf_name': conf_name}
        insRes = self.insert(self.confTab, insert)  
        if insRes == True:
            seq = self.execute("SELECT last_value from configuration_conf_id_seq;")[0][0]
        else: 
            seq = 0
        return seq

    def insertExperiment(self, data):
        """
        insertExperiment    
        """
        if not 'gdb_id' in data:
            if 'gdb_server' in data:
                extension = ' ORDER BY last_update desc LIMIT 1'
                gdbId=self.getId(self.gdbTab, data['gdb_server'], 'gdb_id', 'gdb_name', extension)
                if gdbId:
                    data['gdb_id'] = gdbId
                else:
                    print("ERR: Cannot find {d} in table {t}".format(d=data['gdb_server'], t=self.gdbTab))
                    sys.exit(12)                
            else:
                print("ERR: Cannot insert data, missing parameter gdb_id")
                sys.exit(12)
        if not 'conf_id' in data:
            if 'conf_name' in data:
                confId = self.getId(self.confTab, data['conf_name'], 'conf_id', 'conf_name') 
                if confId:
                    data['conf_id'] = confId
                else:
                    print("ERR: Cannot find {d} in table {t}".format(d=data['conf_name'], t=self.confTab))
                    sys.exit(12)
            else:
                print("ERR: Cannot insert data, missing parameter conf_id")
                sys.exit(12)

        insertData = {'run_date': data['run_date'], 'iteration_count': data['iteration_count'], 'gdb_id': data['gdb_id'], 'conf_id': data['conf_id']}
        insRes = self.insert(self.expTab, insertData)
        if insRes == True:
            seq = self.execute("SELECT last_value from experiment_exper_id_seq;")[0][0]
        else: 
            seq = 0
        return seq

    def insertIteration(self, data):
        """
        insertRecord
        """       
        insertData={'iter_timestamp': data['iter_timestamp'], 'iter_number': data['iter_number'], 'status': data['status'], 'exper_id': data['exper_id']}
        insRes = self.insert(self.iteTab, insertData)
        if insRes == True:
            seq = self.execute("SELECT last_value from iteration_iter_id_seq;")[0][0]
        else: 
            seq = 0
        return seq

    def insertValues(self, data):
        """
        insertValues
        """ 
        for val in data['value']:
            data['meas_id'] = self.getId(self.measTab, val, 'meas_id', 'meas_name') 
            insertData = {'iter_id': data['iter_id'], 'meas_id': data['meas_id'], 'value': data['value'][val]}
            result = self.insert(self.valTab , insertData)
        return "ok"
    
    def insertTypes(self, type_name, conf_id, meas_id):
        """
        insertTypes
        """ 
        insert = {'type_name': type_name, 'conf_id': conf_id, 'meas_id': meas_id}
        insRes = self.insert(self.typeTab, insert)  
        if insRes == True:
            seq = self.execute("SELECT last_value from types_type_id_seq;")[0][0]
        else: 
            seq = 0
        return seq

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
    
    def getReportQuery(self, command=None, database=None, experiment=None, versionDB=None):
        condition = "status='OK'"
        if experiment:
            condition += " AND conf.conf_name='{}'".format(experiment)
        if database:
            condition += " AND gr.gdb_server='{}'".format(database)
        if versionDB:
            condition += " AND gr.gdb_version='{}'".format(versionDB)
        if command:
            condition += " AND ty.type_name='{}'".format(command)
            
        query = REPORT_ITERATION.format(cond=condition)
        print("INFO: Report query: \n\n'{}'\n".format(query))
        return query
    
    def getGraphData(self, command=None, database=None, experiment=None, versionDB=None):
        condition = "status='OK'"
        if experiment:
            condition += " AND conf.conf_name='{}'".format(experiment)
        if database:
            condition += " AND gr.gdb_server='{}'".format(database)
        if versionDB:
            condition += " AND gr.gdb_version='{}'".format(versionDB)
        if command:
            condition += " AND ty.type_name='{}'".format(command)
            
        query = TMP_PNG_DATA.format(cond=condition)
        print("INFO: Report query: \n\n'{}'\n".format(query))
        print("WARN: Only prototype with static query for now!")
        return self.execute(query)
    
    def copyToCSV(self, query, csvFile):
        copyQuery = "COPY ({}) TO STDOUT WITH CSV HEADER".format(query)
        try:
            with self.connection() as cursor:
                with open(csvFile, 'w') as f:
                    cursor.copy_expert(copyQuery, f)
                print("INFO: CSV file was created - {}".format(csvFile))
        finally:
            self.dbConnection.close()
    
    def cleanDB(self):
        databases = [self.gdbTab, self.confTab, self.expTab, self.iteTab, self.valTab]
        for db in databases:
            self.execute('DROP TABLE {}'.format(db))
        

def main():
    print ("---")
    db = {'gdb_name': 'testovaciDB', 'gdb_description': 'Testovaci Databaze', 'gdb_version': '2.5.4'}
    exper = {'run_date': '2017-12-13 00:00:01', 'iteration_count': 3}
    #exper['gdb_id']=1
    exper['gdb_name']='orientdb'
    #exper['conf_id']=1
    exper['conf_name']='e_select_001.conf'
    #value = ['test', '7']
    iteration = {'iter_timestamp': '2017-12-02 00:00:01', 'iter_number': 1, 'status': 'OK', 'exper_id':1}
    mon = Monitoring()
    #mon.insertDatabase(db)
    print(mon.insertExperiment(exper))
    #mon.insertIteration(iteration)
    #mon.insertValue(value)
    #print(mon.select("SELECT * FROM ITERATION;"))
    print(mon.select("SELECT * FROM EXPERIMENT;"))
    print("-")
    #mon.exportTable("graph_databases", "/home/hapina/Downloads" )
    #mon.importTable("/home/hapina/Downloads/e_graph_databases_2017-12-03.csv", "graph_databases")
    
    print ("---")

if __name__ == "__main__":
	main()

