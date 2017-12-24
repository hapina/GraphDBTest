import sys

from setupConf import Configuration
from monitoring.monitoring import Monitoring

directory = sys.argv[1]
conf_name = sys.argv[2]
file = directory + conf_name 
mon = Monitoring()
if not mon.getId(mon.confTab, conf_name, 'conf_id', 'conf_name'):
    exper = Configuration(file)
    exper.setupConf()
    type_ex = exper.get('experiment_type')
    meas_id = 1
    if type_ex:
        conf_id = mon.insertConfiguration(conf_name)
        mon.insertTypes(type_ex, conf_id, meas_id)
