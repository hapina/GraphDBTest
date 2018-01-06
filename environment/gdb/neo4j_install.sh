#!/bin/bash
#
#   neo4j_install.sh
####

# Settings for Neo4j
graphName=neo4j
groupId=org.apache.tinkerpop
artifactId=neo4j-gremlin
version=$1
tmpConfig=conf/${graphName}_x.properties 
graphPath=org.apache.tinkerpop.gremlin.neo4j.structure.Neo4jGraph
location=/temp/gremlin_databases/neo4j

cat <<< "[INFO] Install ${artifactId^}"
cd /opt/gremlin/
ins=`/opt/gremlin/bin/gremlin-server.sh stop && bin/gremlin-server.sh install $groupId $artifactId $version`

[[ -z $ins ]] || echo "[ERR] Install ${artifactId^}:  $ins"

cat <<< "[INFO] Create config: $tmpConfig "
conf=`cat > $tmpConfig <<EOF
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# This is a sample configuration file for ${artifactId^}.  Note that
# TinkerPop does not include ${artifactId^} dependencies in its
# distributions.  To use this file, please ensure that ${artifactId^}
# dependencies are installed into Gremlin Server's path
# with:
#
# gremlin-server.sh -i $groupId $artifactId $version
#
gremlin.graph=$graphPath
gremlin.neo4j.directory=$location
EOF`
[[ -z $conf ]] && cat <<< "[INFO] Installed succeed"
status=`/opt/gremlin/bin/gremlin-server.sh start`
cat <<< "[INFO] Gremlin server: $status"
