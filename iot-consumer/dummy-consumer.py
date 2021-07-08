from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def main():
    spark = SparkSession.builder.appName("Dummy-consumer").getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 10)  # batch interval to collect data
    
    kvs = KafkaUtils.createDirectStream(ssc, ["test"], {"metadata.broker.list": "kafka:9092"})
    lines = kvs.map(lambda line: line)
    lines.pprint()
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
 
