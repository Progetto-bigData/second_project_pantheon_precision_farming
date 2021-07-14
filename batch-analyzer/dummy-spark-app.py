#!/usr/bin/env python3
""" spark application """

import argparse
import time

from pyspark.sql import SparkSession

# create parser and set its arguments
time.sleep(60)
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="Input file path")
parser.add_argument("--output", type=str, help="Output file path")

# parse arguments
args = parser.parse_args()
input_filepath, output_filepath = args.input, args.output

# initialize SparkSession
spark = SparkSession.builder.appName("DummySparkApp").config().getOrCreate()


lines_RDD = spark.sparkContext.textFile(input_filepath)

lines_RDD = lines_RDD.map(lambda x: x.split(",")) 

spark.sparkContext.parallelize(lines_RDD.collect()).saveAsTextFile(output_filepath)


