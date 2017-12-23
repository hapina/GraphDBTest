import sys
import getopt
import seaborn as sns
import matplotlib.pyplot as plt

from monitoring.monitoring import Monitoring 

def main():
    #------------------------------ Processing input arguments     
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:d:e:f:q:", ["command=", "database=", "experiment=", "file=", "query="])
    except getopt.GetoptError as err:
        print (err)
        sys.exit(2)
        
    command = database = experiment = query = fileName = None
    data = ""
    
    for o, a in opts:
        if o in ("-c", "--command"):
            command = a
        elif o in ("-d", "--database"):
            database = a
        elif o in ("-e", "--experiment"):
            experiment = a
        elif o in ("-f", "--file"):
            fileName = a
        elif o in ("-q", "--query"):
            query = a
        else:
            assert False, "unhandled option."
        
    #------------------------------ Generate data for plotting
    m = Monitoring()
    data = m.getGraphData(database)
    if __debug__: 
        print(data)
    plt.plot(data, color='blue', label=database)
    plt.title("Experiment: run_time")
    plt.xlabel("number of iteration")
    plt.ylabel("run_time (seconds)")
    plt.legend()
    plt.savefig(fileName)
    print("INFO: PNG file was created - {}".format(fileName))
    print("WARN: Only prototype with static query for now!")
    
if __name__ == "__main__":
	main()
    
