from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from influxdb import InfluxDBClient
import time
import random
import json

def read_data(x):
    return x


def map_save_influx(x,client):
    values = x[1].encode("utf-8")
    dict_values = json.loads(values)
    print("#####values#######")
    print(dict_values["created"])
    print(dict_values["id_sensor"])
    print(dict_values["type"])
    print(dict_values["value"])
    json_to_save = [
        {
            "measurement": dict_values["id_sensor"],
            "time": dict_values["created"],
            "tags": {
                "sensorType": dict_values["type"]
            },
            "fields": {
                "value": float(dict_values["value"]),
                "unit_measure": dict_values["unit"]
            }
        }
    ]


    client.write_points(json_to_save)
    return x
    

def main():
    time.sleep(35)
    spark = SparkSession.builder.appName("Consumer").getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 10)  # batch interval to collect data
    topics_list = ['humidity-sensor', 'pressure-sensor', 'rain-sensor', 'solar-sensor', 'soil-temperature-sensor', 'soil-water-sensor', 'temperature-sensor', 'wind-sensor']
    kvs = KafkaUtils.createDirectStream(ssc, topics_list, {"metadata.broker.list": "kafka:9092"})
    client = InfluxDBClient(host='influx', port=8086, username='root', password='password')
    client.switch_database('pantheon')
    lines = kvs.map(lambda x: read_data(x)).map(lambda x : map_save_influx(x,client))
    lines.pprint()
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
 
 
