import sys
import getopt
import matplotlib.pyplot as plt
from matplotlib import pylab

from monitoring.monitoring import Monitoring 

def generateSelect(databases, experiment, fileName):
    m = Monitoring()
    for db in databases:
        data = m.getGraphData(experiment, db)
        plt.plot(data, label=db)
    plt.title("Type of experiment: SELECT ({})".format(experiment))
    plt.xlabel("Number of iteration")
    plt.ylabel("Run time in seconds")
    plt.legend()
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))   
    
def generateInsert(experiment, fileName):
    #m = Monitoring()
    #data = m.getGraphData(experiment)
    data = {u'Neo4j':26, u'ArangoDB': 17, u'OrientDB':30}
    plt.bar(range(len(data)), data.values(), align='center')
    plt.xticks(range(len(data)), data.keys())
    plt.title("Type of experiment: INSERT ({})".format(experiment))
    plt.xlabel("Graph databases")
    plt.ylabel("Insert time in seconds")
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))  

def generateImportExport(experiments, fileName):
    #m = Monitoring()
    #data = m.getGraphData(experiment)
    data = {'Neo4j':(26,10), 'ArangoDB': (17,30), 'OrientDB': (30,23)}
    labels=('import','export')
    dim = 2
    w = 0.75
    dimw = w / dim
    x = pylab.arange(len(data.values()))
    for i in range(dim) :
        y = [d[i] for d in data.values()]
        b = plt.bar(x + i * dimw, y, dimw, bottom=0.001, label=labels[i])
    plt.xticks(range(len(data.values())), data.keys())
    plt.title("Type of experiment: IMPORT & EXPORT \n{}".format(experiments))
    plt.xlabel("Graph databases")
    plt.ylabel("Insert time in seconds")
    plt.legend()
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))  
    
def generateCreate(experiment, fileName):
    #m = Monitoring()
    #data = m.getGraphData(experiment)
    data = {u'Neo4j':265.000, u'ArangoDB': 174.000, u'OrientDB': 130.000}
    plt.bar(range(len(data)), data.values(), align='center')
    plt.xticks(range(len(data)), data.keys())
    plt.title("Type of experiment: CREATE ({})".format(experiment))
    plt.xlabel("Graph databases")
    plt.ylabel("Size of new database in KB")
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName)) 


def main():
    #------------------------------ Processing input arguments     
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:d:e:f:q:", ["command=", "database=", "experiment=", "file=", "query="])
    except getopt.GetoptError as err:
        print (err)
        sys.exit(2)
        
    command = experiment = query = None
    databases = ['orientdb', 'neo4j']
    fileName = "/tmp/fig.png"
    data = ""
    
    for o, a in opts:
        if o in ("-c", "--command"):
            command = a
        elif o in ("-d", "--database"):
            databases = [a]
        elif o in ("-e", "--experiment"):
            experiment = a
        elif o in ("-f", "--file"):
            fileName = a
        elif o in ("-q", "--query"):
            query = a
        else:
            assert False, "unhandled option."
        
    #------------------------------ Generate data for plotting
    if command == 'select':
        experiment = "003_select.conf"
        generateSelect(databases, experiment, fileName)
    elif command == 'insert':
        experiment = '002_insert.conf'
        generateInsert(experiment, fileName)
    elif command == 'create':
        experiment = '001_create.conf'
        generateCreate(experiment, fileName)
    elif command in ['import','export']:
        experiment = ['004_export.conf','008_import.conf']
        generateImportExport(experiment, fileName)
    else:
        print("Not implemented yet.")
    
if __name__ == "__main__":
	main()
    
