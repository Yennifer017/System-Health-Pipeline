#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/output"

grep 'SystemHealthMonitor' /var/log/syslog |
awk '
BEGIN{
    OFS=","
    print "Timestamp,Level,CPU,Disk,RAM"
}

{
    timestamp=$1" "$2" "$3

    if(match($0, /(INFO|WARNING|CRITICAL)/))
        level=substr($0,RSTART,RLENGTH)

    if(match($0, /CPU_USAGE=[0-9]+/)){
        cpu=substr($0,RSTART+10,RLENGTH-10)
    }

    if(match($0, /DISK_USAGE=[0-9]+/)){
        disk=substr($0,RSTART+11,RLENGTH-11)
    }

    if(match($0, /RAM_FREE=[0-9]+/)){
        ram=substr($0,RSTART+9,RLENGTH-9)
    }

    print timestamp,level,cpu,disk,ram
}
' > $OUTPUT_DIR/raw_metrics.csv

echo "CSV generated successfully:"
echo "$OUTPUT_DIR/raw_metrics.csv"