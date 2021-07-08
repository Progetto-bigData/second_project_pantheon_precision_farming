import time
from kafka import KafkaProducer

def main():
    time.sleep(10)
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    print(producer)
    print()
    for i in range(10):
        future = producer.send('test', key=b'some_key', value=b'some_bytes')
        time.sleep(10)
        print('sent a message')
        print(i)

if __name__ == "__main__":
    main()
