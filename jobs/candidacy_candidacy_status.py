import pandas as pd
from structlog import get_logger

from jobs.utils.monitoring import job_logging
from jobs.infra.postgresql_connector import PostgreSQLConnector

logging = get_logger()


@job_logging
def expose_candidacy_candidacy_status() -> int:
    candidacy_candidacy_status = read_candidacy_candidacy_status()
    nb_of_records = write_candidacy_candidacy_status_to_postgres(candidacy_candidacy_status)
    return nb_of_records


def read_candidacy_candidacy_status() -> pd.DataFrame:
    pg_connector = PostgreSQLConnector.create_prod_connector()
    candidacy_candidacy_status = pd.read_sql_query(
        sql='''
            SELECT id,
                candidacy_id,
                status,
                created_at,
                updated_at
            FROM candidacy_candidacy_status
        ''',
        con=pg_connector.connection
    )
    logging.info(f'{candidacy_candidacy_status.shape[0]} candidacy_candidacy_status read from reva')
    return candidacy_candidacy_status


def write_candidacy_candidacy_status_to_postgres(candidacy_candidacy_status: pd.DataFrame) -> int:
    pg_connector = PostgreSQLConnector.create_dwh_connector()
    pg_connector.replace_table_data('candidacy_candidacy_status', candidacy_candidacy_status)
    logging.info(
        f'{candidacy_candidacy_status.shape[0]} candidacy_candidacy_status records written to reva-datawarehouse'
    )
    return candidacy_candidacy_status.shape[0]


if __name__ == '__main__':
    expose_candidacy_candidacy_status()
