import json
import asyncio

from kafka import KafkaProducer

from config import kafka_details
from common_funcs import get_logger, split_to_batches


log = get_logger(__name__)


BATCH_SIZE = 50
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


async def on_send_success(record_metadata):
    log.info(f"Message sent topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")


async def on_send_error(exc):
    log.error(f"Error sending message: {exc}")


async def send_single_message(producer, topic, payload, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY_SECONDS, retry_count=0):
    try:
        future = producer.send(topic, value=payload)
        record_metadata = await asyncio.wrap_future(future)
        await on_send_success(record_metadata)
        return True
    except Exception as e:
        retry_count += 1
        await on_send_error(e, payload, retry_count)
        if retry_count < max_retries:
            log.info(f"Retrying message send in {retry_delay} seconds (attempt {retry_count}/{max_retries})...")
            await asyncio.sleep(retry_delay)
            return await send_single_message(producer, topic, payload, max_retries, retry_delay, retry_count)
        else:
            log.error(f"Max retries reached for payload: {payload}. Giving up.")
            return False


async def send_batch(producer, topic, batch, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY_SECONDS):
    send_tasks = [
        send_single_message(producer, topic, payload, max_retries, retry_delay)
        for payload in batch
    ]
    results = await asyncio.gather(*send_tasks)
    successful_sends = sum(results)
    if successful_sends < len(batch):
        log.warning(f"Failed to send {len(batch) - successful_sends} messages in the batch after retries.")


async def send_all_batches(batches, producer):
    for batch in batches:
        await send_batch(producer, kafka_details.kafka_topic, batch)


async def simulate_producer(data):
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_details.kafka_brokers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        log.info(f"Kafka producer connected to {kafka_details.kafka_brokers}")

        batches = split_to_batches(data, BATCH_SIZE)

        await send_all_batches(batches, producer)

    except Exception as error:
        log.error(f"An error occurred: {error}")
        raise error
    finally:
        if 'producer' in locals():
            producer.flush()
            producer.close()
            log.info("Kafka producer closed.")
