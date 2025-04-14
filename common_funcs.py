import logging
import pymysql



def get_logger(name) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )
    return logging.getLogger(name)


def read_file_content(file_name: str) -> str:
    log = get_logger(__name__)
    log.info(f'Reading file {file_name}')
    with open(file_name) as file:
        content = file.read()
    return content


def insert_data(cursor, data, insert_statement, raise_errors=False):
    log = get_logger(__name__)
    try:
        cursor.executemany(insert_statement, data)
        return True
    except pymysql.Error as error:
        if raise_errors:
            raise error
        log.error(f"Error inserting multiple rows into MySQL: {error}")
        return False
    

def split_to_batches(data, batch_size):
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]