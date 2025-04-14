import json
import pymysql

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer

from config import kafka_details, sql_statements
from common_funcs import get_logger, insert_data
from connect_to_db import get_db_con



log = get_logger(__name__)


INSERT_BATCH_SIZE = 100

def consume_and_insert():
    raised_exception = None
    consumer = None
    con = None
    cursor = None
    try:
        consumer = KafkaConsumer(
            kafka_details.kafka_topic,
            bootstrap_servers=kafka_details.kafka_brokers,
            group_id=kafka_details.kafka_group,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'  # Or 'latest', depending on your needs
        )
        log.info(f"Kafka consumer connected to {kafka_details.kafka_brokers} and subscribed to {kafka_details.kafka_topic}")

        con = get_db_con()
        cursor = con.cursor()
        batch_data = []

        for message in consumer:
            try:
                data = message.value
                log.info(f"Received message: {data}")
                batch_data.append(data)

                if len(batch_data) >= INSERT_BATCH_SIZE:
                    if batch_data:
                        if insert_data(cursor, batch_data, sql_statements.insert_statement):
                            con.commit()
                            log.info(f"Inserted {len(batch_data)} records into {kafka_details.target_table}.")
                        else:
                            log.error(f"Failed to insert batch of {len(batch_data)} records.")
                            raised_exception = ValueError(f"Failed to insert batch of data.")
                        batch_data = []  # Clear the batch after processing

            except json.JSONDecodeError as e:
                log.error(f"Error decoding JSON: {message.value.decode('utf-8')}. Error: {e}")
                raised_exception = e
            except Exception as e:
                log.error(f"An unexpected error occurred during message processing: {e}")
                raised_exception = e

        # Process any remaining data in the batch after the consumer loop finishes
        if batch_data:
            if insert_data(cursor, batch_data, sql_statements.insert_statement):
                con.commit()
                log.info(f"Inserted remaining {len(batch_data)} records into {kafka_details.target_table}.")
            else:
                log.error(f"Failed to insert remaining batch of {len(batch_data)} records.")
                raised_exception = ValueError(f"Failed to insert remaining batch of data.")

    except NoBrokersAvailable as e:
        log.error(f"Could not connect to Kafka brokers: {kafka_details.kafka_brokers}. Error: {e}")
        raised_exception = e
    except pymysql.Error as e:
        log.error(f"Database error occurred: {e}")
        raised_exception = e
    except Exception as e:
        log.error(f"An unexpected error occurred in the main consumer loop: {e}")
        raised_exception = e
    finally:
        if consumer:
            consumer.close()
            log.info("Kafka consumer closed.")
        if cursor:
            cursor.close()
            log.info("MySQL cursor closed.")
        if con:
            con.close()
            log.info("MySQL connection closed.")
        if raised_exception:
            log.info('One or more errors were encountered. Latest one will be raised')
            raise raised_exception

if __name__ == "__main__":
    consume_and_insert_batched()