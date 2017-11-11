import configparser

class Configuration:    
    def __init__(self, f = None, d = dict()):
        self.conFile = f
        self.conDict = d
    
    def setupConf(self):
        self.conDict = dict()
        self.readConf()
        
    def updateConf(self):
        self.readConf()
        
    def readConf(self):
        config = configparser.ConfigParser()
        config.read(self.conFile)
        #print (config.sections())        
        for key in config['DEFAULT']: 
            self.conDict.update({key: config['DEFAULT'][key]})
        print (self.conDict)
        return self
    
def main():
    db = Configuration('/home/hapina/graphtest/config/orientdb.conf')
    db.setupConf()
    print (db.conDict['url'])
    
    exper = Configuration('/home/hapina/graphtest/config/expr0001.conf', db.conDict)
    exper.updateConf()
    exper.setupConf()
    print (exper.conDict['queryseq'])
    

if __name__ == "__main__":
	main()
