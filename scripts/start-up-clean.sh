#! /bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
(cd `dirname $0`/../ &&  rm -r ./disk/influxdb_data)
(cd `dirname $0`/../ &&  mkdir ./disk/influxdb_data)
(cd `dirname $0`/../ &&  exec /usr/local/bin/docker-compose up --build --scale consumer=5; cd -) 
 
