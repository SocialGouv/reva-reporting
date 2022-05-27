import pandas as pd
from structlog import get_logger

from jobs.utils.monitoring import job_logging
from jobs.infra.postgresql_connector import ProdPostgreSQLConnector, DWHPostgreSQLConnector

logging = get_logger()


@job_logging
def expose_candidacy() -> int:
    candidacy = read_candidacy()
    nb_of_records = write_candidacy_to_postgres(candidacy)
    return nb_of_records


def read_candidacy() -> pd.DataFrame:
    pg_connector = ProdPostgreSQLConnector()
    candidacy = pd.read_sql_query(
        sql='''
            SELECT id,
                "deviceId",
                keycloak_sub,
                companion_id,
                created_at,
                updated_at,
                certification_id,
                email,
                phone
            FROM candidacy
        ''',
        con=pg_connector.connection
    )
    logging.info(f'{candidacy.shape[0]} candidacy read from reva')
    return candidacy


def write_candidacy_to_postgres(candidacy: pd.DataFrame) -> int:
    pg_connector = DWHPostgreSQLConnector()
    pg_connector.replace_table_data('candidacy', candidacy)
    logging.info(f'{candidacy.shape[0]} candidacy records written to reva-datawarehouse')
    return candidacy.shape[0]


if __name__ == '__main__':
    expose_candidacy()
