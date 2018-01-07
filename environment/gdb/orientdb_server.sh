# !/bin/bash
#
#

[[ $1 == start ]] && /opt/orientdb/bin/server.sh

[[ $1 == stop ]] && /opt/orientdb/bin/shutdown.sh
