from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from influxdb import InfluxDBClient
import time
import random

''' 
    This script has only testing purposes
'''
def read_data(x):
    return x


def map_save_influx(x,client):
    data=x[1]
    seconds = random.randint(0,59)
    json = [
        {
            "measurement": "test",
            "time": "2020-06-05T13:35:" + str(seconds) + ".000Z",
            "fields": {
                "field_test": data,
            }
        }
    ]
    client.write_points(json)
    return x
    

def main():
    time.sleep(30)
    spark = SparkSession.builder.appName("Dummy-consumer").getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 10)  # batch interval to collect data
    
    kvs = KafkaUtils.createDirectStream(ssc, ["test"], {"metadata.broker.list": "kafka:9092"})
    client = InfluxDBClient(host='influx', port=8086, username='root', password='password')
    client.switch_database('pantheon')
    lines = kvs.map(lambda x: read_data(x)).map(lambda x : map_save_influx(x,client))
    lines.pprint()
    #lines.saveAsTextFiles("/datalake/")
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
 
