import sys
import getopt
import matplotlib.pyplot as plt

from monitoring.monitoring import Monitoring 

def generateSelect(databases, experiment, fileName):
    m = Monitoring()
    for db in databases:
        data = m.getGraphData(experiment, db)
        plt.plot(data, label=db)
    plt.title("Type of experiment: SELECT")
    plt.xlabel("Number of iteration")
    plt.ylabel("Time in seconds")
    plt.legend()
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))   
    
def generateInsert(databases, experiment, fileName):
    m = Monitoring()
    for db in databases:
        data = m.getGraphData(experiment, db)
        plt.plot(data, label=db)
    plt.title("Type of experiment: INSERT")
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))  


def main():
    #------------------------------ Processing input arguments     
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:d:e:f:q:", ["command=", "database=", "experiment=", "file=", "query="])
    except getopt.GetoptError as err:
        print (err)
        sys.exit(2)
        
    command = query = None
    databases = ['orientdb', 'neo4j']
    fileName = "/tmp/fig.png"
    experiment = "003_select.conf"
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
        generateSelect(databases, experiment, fileName)
    elif command == 'insert':
        generateInsert(databases, experimnet, fileName)
    else:
        print("Not implemented yet.")
    
if __name__ == "__main__":
	main()
    
