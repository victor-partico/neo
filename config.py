from pandera import DataFrameSchema, Column, Check
from pandera.dtypes import Timestamp
from common_funcs import read_file_content

schema = DataFrameSchema(
            {
                "app_no": Column(
                    int,
                    Check(lambda x: x.notnull()),
                    coerce=True,
                    nullable=False
                ),
                "type": Column(
                    str,
                    [
                        Check(lambda x: x.str.len() == 3),
                        Check(lambda x: x.notnull())
                    ],
                    nullable=False
                ),
                "app_date": Column(
                    Timestamp,
                    coerce=True,
                    nullable=True
                ),
                "status": Column(
                    str,
                    Check(lambda x: x.notnull()),
                    nullable=False
                ),
                "fru_interview_scheduled": Column(str),
                "drug_test": Column(str),
                "wav_course": Column(str),
                "defensive_driving": Column(str),
                "driver_exam": Column(str),
                "medical_clearance_form": Column(str),
                "other_requirements": Column(str),
                "last_updated": Column(
                    Timestamp,
                    coerce=True
                ),
            }
        )

# the two data sources 'dpec-ucu7' and 'dpec-ucu7' have different last column name
# this is used to uniform the names
source_columns_to_rename = {'lastupdate': 'last_updated'}


class NYCOpenDataSourceParams:
    def __init__(self):
        self.domain = 'data.cityofnewyork.us'
        self.new_dateset_id = 'dpec-ucu7'
        self.historical_dateset_id = 'p32s-yqxq'

nyc_open_data_source_params = NYCOpenDataSourceParams()


class MySQLConectionDetails:
    def __init__(self):
        self.host='127.0.0.1'
        self.port=3306
        self.user='root'

mysql_con_details = MySQLConectionDetails()


class MySQLErorCodes:
    def __init__(self):
        self.table_does_not_exist_error_id = 1146

mysq_sql_error_codes = MySQLErorCodes()


class SQLStatements:
    def __init__(self):
        self.target_schema_name = 'neoshare_lake'
        self.target_table_name = 'tlc_new_driver_application_status'

        self.create_target_table_sql = read_file_content('./init_db_tables/neoshare_lake.tlc_new_driver_application_status.sql')
        self.create_processing_view_sql = read_file_content('./init_db_tables/neoshare_mart_v.view_fact_licenses_monthly.sql')
        self.create_mart_table_sql = read_file_content('./init_db_tables/neoshare_mart.fact_licenses_monthly.sql')
        self.create_procedure_sql = read_file_content('./init_db_tables/neoshare_mart_v.RefreshFactLicensesMonthly.sql')
        # self.create_update_tigger_sql = read_file_content('./init_db_tables/neoshare_lake.AfterTlcNewDriverAppStatusUpdate.sql')
        # self.create_insert_tigger_sql = read_file_content('./init_db_tables/neoshare_lake.AfterTlcNewDriverAppStatusInsert.sql')

        self.check_if_inital_load_sql = \
            f"SELECT 1 FROM `{self.target_schema_name}`.`{self.target_table_name}` LIMIT 1"

        self.insert_statement = read_file_content('./sql_statements/insert_template.sql')

sql_statements = SQLStatements()


class KafkaDetails:
    def __init__(self):
        self.kafka_brokers = ['localhost:9092']
        self.kafka_topic = 'driver_application_status'
        self.kafka_group = 'driver_application_status_group'
        self.target_table = f'`{sql_statements.target_schema_name}`.`{sql_statements.target_table_name}`'

kafka_details = KafkaDetails()