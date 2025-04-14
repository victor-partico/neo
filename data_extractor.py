import time
from sodapy import Socrata
from pymysql import ProgrammingError

from config import nyc_open_data_source_params, sql_statements, mysq_sql_error_codes
from connect_to_db import get_logging_db_con
from common_funcs import get_logger


log = get_logger(__name__)

LIMIT_BATCH_SIZE = 10_000
TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5


def extract_data():
    is_initial_load = check_if_initial_load()
    if is_initial_load:
        prepare_lake_table()
        dataset_id = nyc_open_data_source_params.historical_dateset_id
    else:
        dataset_id = nyc_open_data_source_params.new_dateset_id

    all_results = []
    offset = 0

    with Socrata(nyc_open_data_source_params.domain, None, timeout=TIMEOUT) as client:
        while True:
            result = get_bach_data(client, dataset_id, LIMIT_BATCH_SIZE, offset)
    
            if not result:
                break

            all_results.extend(result)
            offset += LIMIT_BATCH_SIZE

    assert all_results, 'No records were returned'

    log.info(f'Extracted data has {len(all_results)} records')
    return all_results


def get_bach_data(client, dataset_id, limit, offset):
    for attempt in range(MAX_RETRIES):
        try:
            result = client.get(dataset_id, limit=limit, offset=offset)
            return result
        except Exception as error:
            log.warning(f'Attempt {attempt + 1} failed with error: {error}')
            if attempt < MAX_RETRIES - 1:
                log.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                log.warning(f"Max retries reached.")
                raise error
    

def prepare_lake_table():
    log.info('Inital run of extracting data, would create target table')
    with get_logging_db_con() as db:
        with db.cursor() as cursor:
            cursor.execute(sql_statements.create_target_table_sql)
            cursor.execute(sql_statements.create_processing_view_sql)
            cursor.execute(sql_statements.create_mart_table_sql)
            cursor.execute(sql_statements.create_procedure_sql)
            # cursor.execute(sql_statements.create_update_tigger_sql)
            # cursor.execute(sql_statements.create_insert_tigger_sql)
        db.commit()


def check_if_initial_load():
    with get_logging_db_con() as db:
        with db.cursor() as cursor:
            try:
                cursor.execute(sql_statements.check_if_inital_load_sql)
                result = cursor.fetchall()
            except ProgrammingError as error:
                if error.args[0] == mysq_sql_error_codes.table_does_not_exist_error_id:
                    log.info(f'Target table does not exist')
                    return True
                else:
                    raise error

    if result:
        log.info(f'Target table exist and has records')
        return False
    else:
        log.info(f'Target table exist, but its empty')
        return True


if __name__ == "__main__":
    extract_data()
