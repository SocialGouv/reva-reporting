import pandas as pd
from structlog import get_logger

from jobs.utils.monitoring import job_logging
from jobs.infra.postgresql_connector import PostgreSQLConnector

logging = get_logger()


@job_logging
def expose_experience() -> int:
    experience = read_experience()
    nb_of_records = write_experience_to_postgres(experience)
    return nb_of_records


def read_experience() -> pd.DataFrame:
    pg_connector = PostgreSQLConnector.create_prod_connector()
    experience = pd.read_sql_query(
        sql='''
            SELECT id,
                description,
                "startedAt",
                candidacy_id,
                created_at,
                updated_at,
                duration,
                title
            FROM experience
        ''',
        con=pg_connector.connection
    )
    logging.info(f'{experience.shape[0]} experience read from reva')
    return experience


def write_experience_to_postgres(experience: pd.DataFrame) -> int:
    pg_connector = PostgreSQLConnector.create_dwh_connector()
    pg_connector.replace_table_data('experience', experience)
    logging.info(f'{experience.shape[0]} experience records written to reva-datawarehouse')
    return experience.shape[0]


if __name__ == '__main__':
    expose_experience()
