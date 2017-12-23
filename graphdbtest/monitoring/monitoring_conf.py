""" MONITORING DB
"""

# access from python
MONITORING_CLIENT = None
MONITORING_URL = "localhost"
MONITORING_PORT = 2424
MONITORING_USER = "technical"
MONITORING_PASS = "password"
MONITORING_DBNAME = "experiment_monitoring"
# tables in database

MONITORING_GDB_TABLE = "GRAPHDB"
MONITORING_MEAS_TABLE = "MEASUREMENT"
MONITORING_CONF_TABLE = "CONFIGURATION"
MONITORING_TYPE_TABLE = "TYPES"
MONITORING_EXP_TABLE = "EXPERIMENT"
MONITORING_ITE_TABLE = "ITERATION"
MONITORING_VAL_TABLE = "MEASUREMENT_VALUE"

TMP_PNG_DATA = "SELECT mv.value FROM measurement_value AS mv LEFT JOIN iteration AS it ON it.iter_id=mv.iter_id WHERE mv.meas_id = 1"
REPORT_PNG_DATA = "SELECT it.iter_number AS \"Number of iteration\","\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'run_time' LIMIT 1) AS \"Time of run\", "\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'start_size' LIMIT 1) AS \"Size DB before\", "\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'end_size' LIMIT 1) AS \"Size DB after\" "\
"FROM iteration AS it "\
"LEFT JOIN experiment AS ex ON ex.exper_id=it.exper_id "\
"LEFT JOIN graphdb AS gr ON gr.gdb_id=ex.gdb_id "\
"LEFT JOIN configuration AS conf ON conf.conf_id=ex.conf_id "\
"LEFT JOIN types AS ty ON ty.conf_id=conf.conf_id "\
"WHERE {cond} "\
"ORDER BY it.iter_id"

REPORT_EXPERIMENT = "SELECT ex.exper_id AS \"ID\", ex.run_date AS \"Datetime\", ex.iteration_count AS \"Count of iteration\", gr.gdb_name AS \"Graph database\", conf.conf_name AS \"Configuration File\" FROM experiment AS ex LEFT JOIN graphdb AS gr ON gr.gdb_id=ex.gdb_id LEFT JOIN configuration AS conf ON conf.conf_id=ex.conf_id"

REPORT_ITERATION = "SELECT it.iter_id AS \"ID\","\
"it.iter_timestamp AS \"Datetime\","\
"ex.exper_id AS \"ExperID\", "\
"ex.iteration_count AS \"Count of iteration\", "\
"it.iter_number AS \"Number of iteration\","\
"gr.gdb_name AS \"Graph database\", "\
"ty.type_name AS \"Type\","\
"conf.conf_name AS \"Configuration File\", "\
"it.status AS \"Status\", "\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'run_time' LIMIT 1) AS \"Time of run\", "\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'start_size' LIMIT 1) AS \"Size DB before\", "\
"(SELECT mv.value "\
"    FROM measurement_value AS mv "\
"    LEFT JOIN measurement AS m ON m.meas_id=mv.meas_id "\
"    WHERE mv.iter_id = it.iter_id "\
"    AND m.meas_name = 'end_size' LIMIT 1) AS \"Size DB after\" "\
"FROM iteration AS it "\
"LEFT JOIN experiment AS ex ON ex.exper_id=it.exper_id "\
"LEFT JOIN graphdb AS gr ON gr.gdb_id=ex.gdb_id "\
"LEFT JOIN configuration AS conf ON conf.conf_id=ex.conf_id "\
"LEFT JOIN types AS ty ON ty.conf_id=conf.conf_id "\
"WHERE {cond} "\
"ORDER BY it.iter_id"
