import sys
import csv
import json
import time
from kafka import KafkaProducer

FILENAME_SOLAR_FMT = './2020-{}-solar.csv'
TOPIC = 'solar-sensor'


def create_producer(hostname, port):
    producerEndpointFmt = '{}:{}'
    return KafkaProducer(bootstrap_servers=producerEndpointFmt.format(hostname,port))


def send_data(producerInstance, topicName, data, month_number):
    producerInstance.send(topicName, data.encode('UTF-8'))
    print('sent a message')
    print(data)
    print(month_number)
    print()
    return


def read_file_and_send_data(producer, month_number):
    filename = FILENAME_SOLAR_FMT.format(month_number)
    with open(filename) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            jsonRow = json.dumps(row)
            send_data(producer, TOPIC, jsonRow, month_number)
            time.sleep(0.1)

    
def main():
    time.sleep(20)
    
    producer = create_producer('kafka', '9092')
    print(producer)
    print()
    
    read_file_and_send_data(producer, '06')
    read_file_and_send_data(producer, '07')
    read_file_and_send_data(producer, '08')
    read_file_and_send_data(producer, '09')
    read_file_and_send_data(producer, '10')
    read_file_and_send_data(producer, '11')
    read_file_and_send_data(producer, '12')


if __name__ == "__main__":
    main()
 
 
