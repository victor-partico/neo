import os
from connect_to_db import get_db_con
from common_funcs import get_logger, insert_data, split_to_batches
from config import sql_statements

from data_extractor import extract_data
from data_validator import DataValidatorAndProcessor

from kafka_produce import simulate_producer
from kafka_consume import consume_and_insert


log = get_logger(__name__)

INSERT_BATCH_SIZE = 200


def main():
    extracted_data = extract_data()
    extracted_data = DataValidatorAndProcessor(extracted_data)

    if os.environ.get('RUN_ENVIRONMENT', 'LOCAL_TEST_RUN') != 'LOCAL_TEST_RUN':
        simulate_producer(extracted_data)
        consume_and_insert()

    else:
        log.info('This is a local test run, igestion would be done directly to DB')
        with get_db_con() as db:
            with db.cursor() as cursor:
                extracted_data = split_to_batches(extracted_data, INSERT_BATCH_SIZE)
                n_batches = len(extracted_data)
                n = 1
                for bacth in extracted_data:
                    log.info(f'Sending bath {n} out of {n_batches}')
                    insert_data(
                        cursor=cursor,
                        data=bacth,
                        insert_statement=sql_statements.insert_statement,
                        raise_errors=True
                    )
                    n+=1

                db.commit()

                cursor.execute('CALL neoshare_mart_v.RefreshFactLicensesMonthly()')
                db.commit()

if __name__ == "__main__":
    main()
