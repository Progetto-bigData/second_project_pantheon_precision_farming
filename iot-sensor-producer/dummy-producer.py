import time
from kafka import KafkaProducer

def main():
    time.sleep(10)
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    print(producer)
    print()
    for i in range(10):
        future = producer.send('test', b'some_bytes')
        time.sleep(1)
        print('sent a message')
        print(i)

if __name__ == "__main__":
    main()
