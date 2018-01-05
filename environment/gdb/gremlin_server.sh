#!/bin/bash
#
#   gremlin_server.sh
####

[[ $1 -ge start ]] && /opt/gremlin/bin/gremlin-server.sh start
[[ $1 -ge stop ]] && /opt/gremlin/bin/gremlin-server.sh stop
