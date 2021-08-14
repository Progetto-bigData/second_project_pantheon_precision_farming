import sys
import csv
import json
import time
from kafka import KafkaProducer
import configFileManager

FILENAME_TEMPERATURE_AVERAGE_FMT = './2020-{}-temperature-average.csv'
FILENAME_TEMPERATURE_MAX_FMT = './2020-{}-temperature-max.csv'
FILENAME_TEMPERATURE_MIN_FMT = './2020-{}-temperature-min.csv'
TOPIC = 'temperature-sensor'

def create_producer(hostname, port):
    producerEndpointFmt = '{}:{}'
    return KafkaProducer(bootstrap_servers=producerEndpointFmt.format(hostname,port))

def send_data(producerInstance, topicName, data, month_number, filename):
    producerInstance.send(topicName, data.encode('UTF-8'))
    print('sent a message')
    print(data)
    print(month_number)
    print(filename)
    print()
    return

def read_file_and_send_data(producer, filenames, month_number):
    timeToSleep = float(configFileManager.read_config_file("DEFAULT", "sleeptimebetweenrows", "properties.ini"))
    for filename in filenames:
        filename = filename.format(month_number)
        with open(filename) as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                jsonRow = json.dumps(row)
                send_data(producer, TOPIC, jsonRow, month_number, filename)
                time.sleep(timeToSleep)
    
def main():
    timeToSleep = int(configFileManager.read_config_file("DEFAULT", "startingsleeptime", "properties.ini"))
    time.sleep(timeToSleep)
    
    producer = create_producer('kafka', '9092')
    print(producer)
    print()
    filenames = [FILENAME_TEMPERATURE_AVERAGE_FMT, FILENAME_TEMPERATURE_MAX_FMT, FILENAME_TEMPERATURE_MIN_FMT]
    
    read_file_and_send_data(producer, filenames, '06')
    read_file_and_send_data(producer, filenames, '07')
    read_file_and_send_data(producer, filenames, '08')
    read_file_and_send_data(producer, filenames, '09')
    read_file_and_send_data(producer, filenames, '10')
    read_file_and_send_data(producer, filenames, '11')
    read_file_and_send_data(producer, filenames, '12')

if __name__ == "__main__":
    main()
 
