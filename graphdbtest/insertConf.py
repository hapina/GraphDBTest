import sys

from monitoring.monitoring import Monitoring

conf_name = sys.argv[1]
mon = Monitoring()
if not mon.getId(mon.confTab, conf_name, 'conf_id', 'conf_name'):
    mon.insertConfiguration(conf_name)
