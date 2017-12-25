import sys

from setupConf import Configuration
from monitoring.monitoring import Monitoring

dictionary = dict()
dictionary['select'] = ['run_time', 'size']
dictionary['create'] = ['run_time', 'size']
dictionary['drop'] = ['run_time', 'size']
dictionary['insert'] = ['run_time', 'size', 'size_after']
dictionary['delete'] = ['run_time', 'size', 'size_after']
dictionary['import'] = ['run_time', 'size']
dictionary['export'] = ['run_time', 'size']

directory = sys.argv[1]
conf_name = sys.argv[2]
file = directory + conf_name 
mon = Monitoring()
if not mon.getId(mon.confTab, conf_name, 'conf_id', 'conf_name'):
    exper = Configuration(file)
    exper.setupConf()
    type_ex = exper.get('experiment_type')
    if type_ex:
        conf_id = mon.insertConfiguration(conf_name)
        for meas_name in dictionary[type_ex]:
            meas_id = mon.getId(mon.measTab, meas_name, 'meas_id', 'meas_name')
            if __debug__:
                print(">>> {cn}: {te} - {mn} - {mi}".format(cn=conf_name, te=type_ex, mn=meas_name, mi=meas_id))
            if meas_id:
                mon.insertTypes(type_ex, conf_id, meas_id)
