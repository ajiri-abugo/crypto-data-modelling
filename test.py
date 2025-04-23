import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance() \
        .in_streaming_mode() \
        .build()
    
    tbl_evn = StreamTableEnvironment.create(stream_execution_environment=env, environment_settings=settings)
    
    kafka_jar = os.path.join(os.path.dirname(__file__), 'flink-sql-connector-kafka_2.11-1.13.0.jar')

    tbl_evn.get_config() \
        .get_configuration() \
        .set_string("pipeline.jars", "file://{}".format(kafka_jar))
    
    src_ddl = """
            CREATE TABLE crypto_data (
                id INT,
                name VARCHAR(51),
                symbol VARCHAR(11),
                date_added TIMESTAMP,
                price DECIMAL(20, 10),
                volume_24h DECIMAL(20, 10),
                volume_change_24h DECIMAL(20, 10),
                max_supply DECIMAL(20, 10),
                circulating_supply DECIMAL(20, 10),
                total_supply DECIMAL(20, 10),
                infinite_supply DECIMAL(20, 10),
                cmc_rank INT,
                last_updated TIMESTAMP
        ) WITH (
                'connector' = 'kafka',
                'topic' = 'crypto_data',
                'properties.bootstrap.servers' = 'localhost:9092',
                'properties.group.id' = 'cryptoData',
                'format' = 'json'
                )
                """
    tbl_evn.execute_sql(src_ddl)

    tbl = tbl_evn.from_path("crypto_data")

    tbl.print_schema()

    sql = """
            SELECT id, name, price AS crypto_price FROM crypto_data WHERE name = 'Bitcoin'
            """
    data = tbl_evn.sql_query(sql)

    print('\nProcess Sink Schema')
    data.print_schema()

if __name__ == "__main__":
    main()